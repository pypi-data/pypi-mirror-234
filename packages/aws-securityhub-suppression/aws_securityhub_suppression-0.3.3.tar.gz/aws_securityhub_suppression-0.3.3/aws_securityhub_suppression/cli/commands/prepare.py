import click
from landingzone_organization import AWSOrganization, Account

from aws_securityhub_suppression import Workload
from aws_securityhub_suppression.cli import Context
from aws_securityhub_suppression.workload_generator import WorkloadGenerator


@click.command()
@click.pass_obj
@click.argument("config-path")
@click.argument("ou-path")
def cli(ctx: Context, config_path: str, ou_path: str) -> None:
    """
    Prepare the folder structure based on the organisation structure.
    """
    ctx.info("Prepare the folder structure based on the organisation structure")
    ctx.debug("Reading the AWS Organizations")
    organization = AWSOrganization(ctx.session).parse()

    workloads = organization.workloads(ou_path.split("/"))
    ctx.debug(f"\tFound {len(workloads)} workloads")

    def handle_workload(workload: Workload) -> None:
        WorkloadGenerator(config_path=config_path, workload=workload).execute()

    list(map(handle_workload, workloads))
