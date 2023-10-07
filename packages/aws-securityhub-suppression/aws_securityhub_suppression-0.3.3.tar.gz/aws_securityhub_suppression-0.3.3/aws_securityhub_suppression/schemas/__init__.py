import os
import yaml
from jsonschema import validate


schema_path = os.path.dirname(os.path.abspath(__file__))


class InvalidSchemaException(Exception):
    def __init__(self, file: str, message: str):
        self.file = file
        self.message = message
        super().__init__(self.message)


def load_schema(file: str) -> dict:
    with open(os.path.join(schema_path, file), "r") as f:
        return yaml.safe_load(f)


def safe_load_file(schema: dict, file_path: str) -> dict:
    try:
        with open(file_path, "r") as f:
            data = yaml.safe_load(f)
            validate(instance=data, schema=schema)
    except Exception as exc:
        raise InvalidSchemaException(file_path, str(exc))

    return data


WorkloadSchema = load_schema("workload.yaml")
EnvironmentSchema = load_schema("environment.yaml")
