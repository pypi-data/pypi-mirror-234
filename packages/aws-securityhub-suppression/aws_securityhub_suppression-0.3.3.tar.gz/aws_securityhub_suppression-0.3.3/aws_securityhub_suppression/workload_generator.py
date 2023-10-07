import os
import yaml
from landingzone_organization.workload import Workload
from aws_securityhub_suppression import Account


class WorkloadGenerator:
    def __init__(self, config_path: str, workload: Workload) -> None:
        self.__config_path = config_path
        self.__workload = workload

    def execute(self) -> None:
        path = os.path.abspath(os.path.join(self.__config_path, self.__workload.name))
        self.__prepare_workload_folder(path)

    @staticmethod
    def __ensure_folder(path: str) -> None:
        if not os.path.isdir(path):
            os.mkdir(path)

    def __resolve_workload_info(self, file: str) -> dict:
        info = {
            "Name": self.__workload.name,
            "Environments": self.__workload.environments,
        }

        if os.path.isfile(file):
            with open(file, "r") as fh:
                info = yaml.safe_load(fh)
                info["Name"] = self.__workload.name
                info["Environments"] = self.__workload.environments

        return info

    @staticmethod
    def __resolve_account_info(account: Account) -> dict:
        return {
            "Name": account.name,
            "AccountId": account.account_id,
            "Suppressions": [],
        }

    def __prepare_workload_folder(self, path: str) -> None:
        self.__ensure_folder(path)
        file = os.path.join(path, "info.yaml")
        info = self.__resolve_workload_info(file)

        with open(file, "w") as fh:
            yaml.dump(info, fh, sort_keys=False)

        for account in self.__workload.accounts:
            environment_file = os.path.join(path, f"{account.environment}.yaml")

            if not os.path.isfile(environment_file):
                with open(environment_file, "w") as fh:
                    yaml.dump(self.__resolve_account_info(account), fh, sort_keys=False)
