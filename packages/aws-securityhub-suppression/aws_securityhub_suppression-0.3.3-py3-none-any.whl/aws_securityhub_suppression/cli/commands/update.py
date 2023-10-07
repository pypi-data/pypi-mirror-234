import click

from aws_securityhub_suppression import load_workloads
from aws_securityhub_suppression.cli import Context
from aws_securityhub_suppression.documentation_generator import DocumentationGenerator
from aws_securityhub_suppression.suppress_findings import SuppressFindings


@click.group()
def cli() -> None:
    """
    Execute the suppression script
    """
    pass


@cli.command()  # type: ignore
@click.pass_obj
@click.argument("config-path")
def suppression(ctx: Context, config_path: str) -> None:
    """
    Suppress all registered findings for all workloads
    """
    ctx.info("Suppress all registered findings for all workloads")
    ctx.debug(f"Reading {config_path}")
    click.echo("Suppress all registered findings for the following workloads:")
    workloads = load_workloads(config_path)

    for workload in workloads:
        click.echo(f"\tWorkload: {workload.name}")
        SuppressFindings(
            client=ctx.session.client("securityhub"), workload=workload
        ).execute()


@cli.command()  # type: ignore
@click.pass_obj
@click.argument("template-path")
@click.argument("config-path")
def docs(ctx: Context, template_path: str, config_path: str) -> None:
    """
    Generate suppression documentation for all workloads
    """
    ctx.info("Generate suppression documentation for the following workloads:")
    workloads = load_workloads(config_path)

    for workload in workloads:
        ctx.info(f"\tWorkload: {workload.name}")
        DocumentationGenerator(
            template_path=template_path, config_path=config_path, workload=workload
        ).render()
