from typing import Optional
import boto3
import click
from boto3 import Session


class Context:
    __profile: str = ""

    def __init__(self, debug: bool, profile: Optional[str]) -> None:
        self.__debug = debug
        self.profile = profile or ""

    @property
    def session(self) -> Session:
        if self.profile:
            return boto3.session.Session(profile_name=self.profile)

        return boto3.session.Session()

    @property
    def profile(self) -> str:
        return self.__profile

    @profile.setter
    def profile(self, value: str) -> None:
        self.debug(f"AWS profile: {value} is used for this session")
        self.__profile = value

    def debug(self, message: str) -> None:
        if self.__debug:
            click.echo(message)

    @staticmethod
    def info(message: str) -> None:
        click.echo(message)
