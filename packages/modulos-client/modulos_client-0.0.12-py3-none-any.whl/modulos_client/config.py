from contextlib import contextmanager
import os
from typing import Dict, Generator, Optional
import click
from pydantic import BaseModel

import requests
import yaml


MODULOS_CONFIG_FILE = os.path.expanduser("~/.modulos/conf.yml")


class ModulosClient:
    @classmethod
    def from_conf_file(cls):
        with get_modulos_config() as config:
            if config.active_profile is None:
                raise ValueError("No active profile.")
            profile = config.get_active_profile()
            return cls(profile.host, profile.token)

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


class ModulosProfile(BaseModel):
    name: str
    host: str
    token: str


class ModulosConfig(BaseModel):
    active_profile: None | str
    profiles: Dict[str, ModulosProfile]

    def add_profile(self, name: str, host: str, token: str):
        if name in self.profiles:
            click.echo(f"Profile '{name}' already exists. Do you want to overwrite it?")
            if not click.confirm("Overwrite?", abort=False):
                return None
        self.profiles[name] = ModulosProfile(name=name, host=host, token=token)
        self.active_profile = name

    def remove_profile(self, name: str):
        if name not in self.profiles:
            raise ValueError(f"Profile '{name}' does not exist.")
        del self.profiles[name]
        if name == self.active_profile:
            if len(self.profiles) == 0:
                self.active_profile = None
            else:
                # Set the first profile as active profile.
                self.active_profile = list(self.profiles.keys())[0]

    def get_active_profile(self) -> ModulosProfile:
        if self.active_profile is None:
            raise ValueError("No active profile. Please Login first.")
        return self.profiles[self.active_profile]

    def save_to_file(self, file_path) -> None:
        with open(file_path, "w") as f:
            yaml.dump(self.model_dump(), f)
        return None

    @classmethod
    def from_file(cls, file_path: str) -> "ModulosConfig":
        with open(file_path, "r") as f:
            conf = yaml.safe_load(f)
            return cls(**conf)


@contextmanager
def get_modulos_config() -> Generator[ModulosConfig, None, None]:
    if not os.path.exists(MODULOS_CONFIG_FILE):
        config = ModulosConfig(active_profile=None, profiles={})
        if not os.path.exists(os.path.dirname(MODULOS_CONFIG_FILE)):
            os.makedirs(os.path.dirname(MODULOS_CONFIG_FILE))
    else:
        config = ModulosConfig.from_file(MODULOS_CONFIG_FILE)
    try:
        yield config
    except Exception as e:
        raise e
    else:
        config.save_to_file(MODULOS_CONFIG_FILE)
