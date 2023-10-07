from __future__ import annotations


class Finding:
    def __init__(self, name: str, finding_arn: str) -> None:
        parts = finding_arn.split(":")
        self.__name = name
        self.__finding_arn = finding_arn
        self.__service = parts[2]
        self.__region = parts[3]
        self.__account_id = parts[4]
        self.__finding_id = parts[-1].split("/")[-1]
        self.__generator_id = "/".join(finding_arn.split("/")[1:-2])

    @property
    def name(self) -> str:
        return self.__name

    @property
    def arn(self) -> str:
        return self.__finding_arn

    @property
    def id(self) -> str:
        return self.__finding_id

    @property
    def generator_id(self) -> str:
        return self.__generator_id

    @property
    def region(self) -> str:
        return self.__region

    @property
    def account_id(self) -> str:
        return self.__account_id

    @property
    def service(self) -> str:
        return self.__service

    @property
    def product_arn(self) -> str:
        return f"arn:aws:securityhub:{self.region}::product/aws/securityhub"

    def __str__(self) -> str:
        return self.__finding_arn

    @staticmethod
    def from_dict(data: dict) -> Finding:
        return Finding(name=data["Name"], finding_arn=data["FindingArn"])
