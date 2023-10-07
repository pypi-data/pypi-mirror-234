from typing import List, Optional
import glob
import os
from landingzone_organization.workload import Workload
from aws_securityhub_suppression.account import Account
from aws_securityhub_suppression.schemas import (
    WorkloadSchema,
    EnvironmentSchema,
    safe_load_file,
)
from aws_securityhub_suppression.suppression import Suppression
from aws_securityhub_suppression.finding import Finding


__version__ = "0.3.3"


def load_workloads(workload_path: str) -> List[Workload]:
    workloads = glob.glob(os.path.join(workload_path, "**/info.yaml"), recursive=True)

    def load_workload(file: str) -> Optional[Workload]:
        return load_workload_by_file(file)

    response = list(map(load_workload, workloads))

    return list(filter(None, response))


def load_environments_by_file(path: str) -> Optional[Account]:
    data = safe_load_file(EnvironmentSchema, path)
    return Account.from_dict(data)


def load_workload_by_file(path: str) -> Optional[Workload]:
    data = safe_load_file(WorkloadSchema, path)

    def convert_environments_to_file_locations(environment: str) -> str:
        return os.path.join(os.path.dirname(path), f"{environment}.yaml")

    accounts_files = list(
        map(convert_environments_to_file_locations, data.get("Environments", []))
    )
    response = list(map(load_environments_by_file, accounts_files))
    accounts = list(filter(None, response))

    return Workload.from_dict(data, accounts)
