import glob
import os.path
import click


from aws_securityhub_suppression.cli import Context
from aws_securityhub_suppression.schemas import (
    safe_load_file,
    WorkloadSchema,
    EnvironmentSchema,
    InvalidSchemaException,
)


@click.command()
@click.pass_obj
@click.argument("path")
def cli(ctx: Context, path: str) -> None:
    """
    Validate the listed suppression's
    """
    ctx.debug(f"Path: {path}")

    if not os.path.isdir(path):
        click.echo(f"{path} is not a valid path")
        raise click.Abort(f"{path} is not a valid path")

    workloads = glob.glob(os.path.join(path, "**/info.yaml"), recursive=True)

    try:
        for workload in workloads:
            ctx.debug(f"Validating workload: {workload}")
            data = safe_load_file(WorkloadSchema, workload)

            for environment in data.get("Environments", []):
                environment = os.path.join(
                    os.path.dirname(workload), f"{environment}.yaml"
                )
                ctx.debug(f"Validating environment: {environment}")
                safe_load_file(EnvironmentSchema, environment)

    except InvalidSchemaException as exc:
        message = f"In {exc.file} we detected the following violation:"
        print(message)
        print("=" * len(message))
        print(exc)

        raise click.Abort(exc)
