import tomllib
import click

from resumer import auto_awesome_tex, auto_generate

@click.group()
def cli():
    pass

@cli.command()
@click.argument("data")
@click.option("--filter", "-f")
@click.option("--output", "-o", default="output/output.pdf")
def awesome(data, filter, output):
    auto_awesome_tex(
        data=data,
        filter_config=filter,
        output=output
    )

@cli.command()
@click.argument("config")
@click.argument("data")
def make(config, data):
    with open(config, "rb") as file:
        config = tomllib.load(file)

    engineConfig = config.pop("engine")
    filterConfig = config.pop("filter")

    auto_generate(
        engine_config=engineConfig,
        data=data,
        filter_config=filterConfig
    )


if __name__ == "__main__":
    cli()