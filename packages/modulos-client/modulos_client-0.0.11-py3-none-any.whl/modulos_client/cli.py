# --------------------------------------------------- #
# Copyright (C) 2023 Modulos AG. All rights reserved. #
# --------------------------------------------------- #
import mimetypes
import os
from typing import Dict, Optional

import click
import requests
import tabulate
import yaml


class ModulosClient:
    @classmethod
    def from_conf_file(cls):
        modulos_conf_file = os.path.expanduser("~/.modulos/conf.yml")
        if not os.path.exists(modulos_conf_file):
            click.echo("The conf.yml file does not exist. Please login first.")
            return None

        host = yaml.load(open(modulos_conf_file, "r"), Loader=yaml.FullLoader)["host"]

        token = yaml.load(open(modulos_conf_file, "r"), Loader=yaml.FullLoader)["token"]
        return cls(host, token)

    def __init__(self, host: str = "", token: str = ""):
        self.host = host + "/api"
        self.token = token

    def post(
        self,
        endpoint: str,
        url_params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        files: Optional[Dict] = None,
    ):
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
        api_url = f"{self.host}{endpoint}"

        if url_params:
            api_url += "?" + "&".join([f"{k}={v}" for k, v in url_params.items()])

        response = requests.post(
            api_url,
            headers={"Authorization": f"Bearer {self.token}"},
            json=data,
            files=files,
        )
        return response

    def get(self, endpoint: str, data: Optional[Dict] = None):
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
        api_url = f"{self.host}{endpoint}"
        response = requests.get(
            api_url,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
            json=data,
        )
        return response

    def delete(
        self,
        endpoint: str,
        url_params: Optional[Dict] = None,
        data: Optional[Dict] = None,
    ):
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
        api_url = f"{self.host}{endpoint}"

        if url_params:
            api_url += "?" + "&".join([f"{k}={v}" for k, v in url_params.items()])

        response = requests.delete(
            api_url,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
            json=data,
        )
        return response


@click.group()
def main():
    pass


@main.command(
    help=(
        "Login to the Modulos platform. HOST is the address of the platform. "
        "For local use, this is http://localhost."
    ),
)
@click.argument(
    "host",
    type=str,
)
@click.option(
    "-t",
    "--token",
    prompt=True,
    hide_input=True,
)
def login(host: str, token: str):
    """Login to the Modulos platform. HOST is the address of the platform.
    For local use, this is http://localhost.

    Args:
        host (str): The address of the platform.
        token (str): The token.
    """
    host = host.rstrip("/")
    data = {"host": host, "token": token}

    # Create the config file.
    modulos_conf_file_folder = os.path.expanduser("~/.modulos")
    if not os.path.exists(modulos_conf_file_folder):
        os.makedirs(modulos_conf_file_folder)
    with open(os.path.join(modulos_conf_file_folder, "conf.yml"), "w") as f:
        yaml.dump(data, f)
    return None


@main.command(
    help="Logout from the Modulos platform.",
)
def logout():
    modulos_conf_file = os.path.expanduser("~/.modulos/conf.yml")
    if not os.path.exists(modulos_conf_file):
        click.echo("Logout failed. You are not logged in.")
        return None
    os.remove(modulos_conf_file)
    click.echo("Logout successful.")


@main.group(
    help="Manage organizations.",
)
def orgs():
    pass


@orgs.command(
    "list",
    help="List all organizations.",
)
def list_orgs():
    client = ModulosClient.from_conf_file()
    response = client.get("/organizations", {})
    if response.ok:
        click.echo(tabulate.tabulate(response.json().get("items"), headers="keys"))
    else:
        click.echo(f"Could not list organizations: {response.text}")


@orgs.command(
    "create",
    help="Create a new organization.",
)
@click.option(
    "--name",
    type=str,
    prompt=True,
)
def create_orgs(name: str):
    client = ModulosClient.from_conf_file()
    response = client.post("/organizations", url_params={"organization_name": name})
    if response.ok:
        click.echo(f"Organization '{name}' created.")
    else:
        click.echo(f"Could not create organization: {response.json().get('detail')}")


@orgs.command(
    "delete",
    help="Delete an organization.",
)
@click.option(
    "--name",
    type=str,
    prompt=True,
)
def delete_orgs(name: str):
    client = ModulosClient.from_conf_file()
    response = client.delete("/organizations", url_params={"organization_name": name})
    if response.ok:
        click.echo(f"Organization '{name}' deleted.")
    else:
        click.echo(f"Could not delete organization: {response.json().get('detail')}")


@main.group(
    help="Manage users.",
)
def users():
    pass


@users.command(
    "list",
    help="List all users.",
)
@click.option(
    "-o",
    "--organization-id",
    type=str,
    default=None,
)
def list_users(organization_id: Optional[str] = None):
    client = ModulosClient.from_conf_file()
    if organization_id is None:
        org_id = client.get("/users/me", {}).json().get("organization")["id"]
    else:
        org_id = organization_id
    response = client.get(f"/organizations/{org_id}/users", {})
    if response.ok:
        results = response.json().get("items")
        results = [
            {
                "id": result["id"],
                "organization": result["organization"]["name"],
                "firstname": result["firstname"],
                "lastname": result["lastname"],
                "email": result["email"],
                "is_super_admin": result["is_super_admin"],
                "is_active": result["is_active"],
            }
            for result in results
        ]
        click.echo(tabulate.tabulate(results, headers="keys"))
    else:
        click.echo(f"Could not list users: {response.text}")


@users.command(
    "create",
    help="Create a new user.",
)
@click.option(
    "--organization",
    type=str,
    prompt=True,
)
@click.option(
    "--firstname",
    type=str,
    prompt=True,
)
@click.option(
    "--lastname",
    type=str,
    prompt=True,
)
@click.option(
    "--email",
    type=str,
    prompt=True,
)
@click.option(
    "--azure-oid",
    type=str,
    prompt=True,
)
@click.option(
    "--is-active",
    type=bool,
    prompt=True,
)
def create_users(
    organization: str,
    firstname: str,
    lastname: str,
    email: str,
    azure_oid: str,
    is_active: bool,
):
    client = ModulosClient.from_conf_file()
    org_id = [
        org["id"]
        for org in client.get("/organizations", {}).json()["items"]
        if org["name"] == organization
    ][0]
    response = client.post(
        f"/organizations/{org_id}/users",
        data={
            "organization_name": organization,
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "azure_oid": azure_oid,
            "is_active": is_active,
        },
    )
    if response.ok:
        click.echo(f"User '{email}' created.")
    else:
        click.echo(f"Could not create user: {response.json().get('detail')}")


@users.command(
    "add-role",
    help="Add a role to a user.",
)
@click.option(
    "--user-id",
    type=str,
    prompt=True,
    help="The user ID. You can look it up with 'modulos users list'.",
)
@click.option(
    "--role",
    type=str,
    help="The role to add. Can be 'owner', 'editor', 'viewer' and 'auditor'.",
    prompt=True,
)
@click.option(
    "--project-id",
    type=str,
    prompt=True,
)
@click.option(
    "--organization-id",
    type=str,
    default=None,
)
def add_users_role(
    user_id: str, role: str, project_id: str, organization_id: Optional[str] = None
):
    client = ModulosClient.from_conf_file()
    response = client.post(
        f"/users/{user_id}/roles",
        url_params={
            "role": role,
            "project_id": project_id,
        },
    )
    if response.ok:
        click.echo(f"Role '{role}' added to user '{user_id}'.")
    else:
        click.echo(f"Could not add role to user: {response.json().get('detail')}")


@main.group(
    help="Manage projects.",
)
def projects():
    pass


@projects.command(
    "list",
    help="List all projects.",
)
@click.option(
    "--page",
    type=int,
    default=1,
)
def list_projects(page: int):
    client = ModulosClient.from_conf_file()
    response = client.get("/projects", data={"page": page})
    if response.ok:
        results = response.json().get("items")
        click.echo("\n\nPage: " + str(response.json().get("page")))
        results = [
            {
                "id": result["id"],
                "organization": result["organization"]["name"],
                "name": result["name"],
                "description": result["description"],
            }
            for result in results
        ]
        click.echo(tabulate.tabulate(results, headers="keys"))
    else:
        click.echo(f"Could not list projects: {response.text}")


@projects.command(
    "delete",
    help="Delete a project.",
)
@click.option(
    "--id",
    type=str,
    prompt=True,
)
def delete_projects(id: str):
    client = ModulosClient.from_conf_file()
    response = client.delete(f"/projects/{id}")
    if response.ok:
        click.echo(f"Project '{id}' deleted.")
    else:
        click.echo(f"Could not delete project: {response.json().get('detail')}")


@main.group(
    help="Manage templates.",
)
def templates():
    pass


@templates.command(
    "list",
    help="List all templates.",
)
@click.option(
    "-o",
    "--organization-id",
    type=str,
    default=None,
)
def list_templates(organization_id: Optional[str] = None):
    client = ModulosClient.from_conf_file()
    if organization_id is None:
        org_id = client.get("/users/me", {}).json().get("organization")["id"]
    else:
        org_id = organization_id
    response = client.get(f"/organizations/{org_id}/templates", {})
    if response.ok:
        results = [
            {
                "framework_code": result["framework_code"],
                "framework_name": result["framework_name"],
                "framework_description": result["framework_description"],
                "framework_flag_icon": result["framework_flag_icon"],
                "number_of_requirements": result["number_of_requirements"],
                "number_of_controls": result["number_of_controls"],
            }
            for result in response.json()
        ]
        click.echo(tabulate.tabulate(results, headers="keys"))
    else:
        click.echo(f"Could not list templates: {response.text}")


@templates.command(
    "upload",
    help="Upload templates for your organization.",
)
@click.option(
    "--file",
    type=str,
    prompt=True,
)
@click.option(
    "-o",
    "--organization-id",
    type=str,
    default=None,
)
def upload_templates(file: str, organization_id: Optional[str] = None):
    client = ModulosClient.from_conf_file()
    if organization_id is None:
        org_id = client.get("/users/me", {}).json().get("organization")["id"]
    else:
        org_id = organization_id
    with open(file, "rb") as f:
        files = {"file": (file, f, mimetypes.guess_type(file)[0])}
        response = client.post(
            f"/organizations/{org_id}/templates",
            files=files,
        )
    if response.ok:
        click.echo(f"Templates uploaded.")
    else:
        click.echo(f"Could not upload templates: {response.text}")


if __name__ == "__main__":
    main()
