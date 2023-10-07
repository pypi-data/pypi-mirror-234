from jinja2 import Environment, FileSystemLoader
from aws_securityhub_suppression import Workload
import os


class DocumentationGenerator:
    def __init__(
        self, template_path: str, config_path: str, workload: Workload
    ) -> None:
        self.__template_path = template_path
        self.__config_path = config_path
        self.__workload = workload

    @property
    def template_path(self) -> str:
        return os.path.dirname(self.__template_path)

    @property
    def template_file(self) -> str:
        return os.path.basename(self.__template_path)

    def render(self) -> None:
        workload_readme_path = os.path.abspath(
            os.path.join(self.__config_path, self.__workload.name, "README.md")
        )

        with open(workload_readme_path, "w") as f:
            f.write(self.__parse_template(workload=self.__workload))

    def __parse_template(self, workload: Workload) -> str:
        environment = Environment(loader=FileSystemLoader(self.template_path))
        results_template = environment.get_template(self.template_file)
        return results_template.render(workload=workload)
