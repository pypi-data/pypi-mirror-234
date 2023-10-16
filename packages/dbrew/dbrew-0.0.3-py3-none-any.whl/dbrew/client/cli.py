import click
import os

from dbrew.core.validate.schema import YamlValidator, DataProductSchema


@click.group(name="dbrew")
def cli():
    pass


@cli.command()
@click.option("--path", default="dataproduct.yaml", help="Path to the YAML file")
def brew(path):
    # Check if the file exists
    if not os.path.exists(path):
        click.echo(f"Error: File {path} not found")
        return

    # validate the yaml data using the dbrew.core.validate.schema.YamlValidator class
    validator = YamlValidator(path)
    try:
        dataproduct_schema: DataProductSchema = validator.validate_file()
        click.echo(f"Validation successful for {dataproduct_schema.product.name}")
    except Exception as e:
        click.echo(f"Error: {e}")
        return


if __name__ == "__main__":  # pragma: no cover
    # Add the help option to the CLI
    cli.add_command(cli.help)

    # Run the CLI
    cli()
