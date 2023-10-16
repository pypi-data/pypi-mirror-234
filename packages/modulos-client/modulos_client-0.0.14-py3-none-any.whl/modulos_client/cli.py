# --------------------------------------------------- #
# Copyright (C) 2023 Modulos AG. All rights reserved. #
# --------------------------------------------------- #
import mimetypes
from typing import Optional

import click
import tabulate

from modulos_client import config as config_utils


@click.group()
def main():
    pass


@main.command(
    help=(
        "Login to the Modulos platform. HOST is the address of the platform. "
        "For local use, this is http://localhost."
    ),
)
@click.option(
    "-h",
    "--host",
    type=str,
    prompt=True,
)
@click.option(
    "-t",
    "--token",
    prompt=True,
    hide_input=True,
)
@click.option(
    "-p",
    "--profile-name",
    type=str,
    prompt=True,
    help=(
        "The name of the profile. It is used to reference the profile in the "
        "future. If you want to use multiple profiles, you can specify a "
        "different name for each profile."
    ),
)
def login(host: str, token: str, profile_name: str):
    """Login to the Modulos platform. HOST is the address of the platform.
    For local use, this is http://localhost.

    Args:
        host (str): The address of the platform.
        token (str): The token.
        profile_name (str): The name of the profile. If you want to use multiple
            profiles, you can specify a different name for each profile.
    """
    host = host.rstrip("/")
    with config_utils.get_modulos_config() as config:
        config.add_profile(profile_name, host, token)
    return None


@main.command(
    help="Logout from the Modulos platform on all profiles.",
)
def logout():
    with config_utils.get_modulos_config() as config:
        click.echo("This will remove all profiles. Do you want to continue?")
        if not click.confirm("Continue?", abort=False):
            return None
        for profile_name in config.profiles:
            config.remove_profile(profile_name)
    click.echo("Logout successful.")


@main.group(
    help="Manage profiles.",
)
def profiles():
    pass


@profiles.command(
    "list",
    help="List all profiles.",
)
def list_profiles():
    with config_utils.get_modulos_config() as config:
        if config.active_profile is None:
            click.echo("No profiles.")
        else:
            active_profile = config.active_profile
            profile_details = []
            for profile_name, profile in config.profiles.items():
                if profile_name == active_profile:
                    profile_name = f"{profile_name} (active)"

                profile_details.append([profile_name, profile.host])
            headers = ["Name", "Host"]
            click.echo(
                tabulate.tabulate(
                    profile_details, headers=headers, tablefmt="fancy_grid"
                )
            )


@profiles.command(
    "activate",
    help="Activate a profile.",
)
@click.option(
    "-p",
    "--profile-name",
    type=str,
    prompt=True,
    help=("The name of the profile to activate."),
)
def activate_profile(profile_name: str = "default"):
    with config_utils.get_modulos_config() as config:
        if config.profiles is None:
            click.echo("No profiles.")
        elif profile_name not in config.profiles:
            click.echo(f"Profile '{profile_name}' does not exist.")
        else:
            config.active_profile = profile_name
            click.echo(f"Profile '{profile_name}' activated.")


@profiles.command(
    "deactivate",
    help="Remove a profile.",
)
@click.option(
    "-p",
    "--profile-name",
    type=str,
    prompt=True,
    help="The name of the profile to deactivate.",
)
def deactivate_profile(profile_name: str):
    with config_utils.get_modulos_config() as config:
        if config.profiles is None:
            click.echo("No profiles.")
        elif profile_name not in config.profiles:
            click.echo(f"Profile '{profile_name}' does not exist.")
        else:
            config.remove_profile(profile_name)
            click.echo(f"Profile '{profile_name}' deactivated.")
            if config.active_profile is not None:
                click.echo(
                    f"Profile '{config.active_profile}' is now the active profile."
                )
            else:
                click.echo("No active profile anymore.")


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
    client = config_utils.ModulosClient.from_conf_file()
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
    client = config_utils.ModulosClient.from_conf_file()
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
    client = config_utils.ModulosClient.from_conf_file()
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
    client = config_utils.ModulosClient.from_conf_file()
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
    client = config_utils.ModulosClient.from_conf_file()
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
    client = config_utils.ModulosClient.from_conf_file()
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
    client = config_utils.ModulosClient.from_conf_file()
    org_id = client.get("/users/me", {}).json().get("organization")["id"]
    response = client.get(f"/organizations/{org_id}/projects", data={"page": page})
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
    client = config_utils.ModulosClient.from_conf_file()
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
    client = config_utils.ModulosClient.from_conf_file()
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
    client = config_utils.ModulosClient.from_conf_file()
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
        click.echo("Templates uploaded.")
    else:
        click.echo(f"Could not upload templates: {response.text}")


if __name__ == "__main__":
    main()
