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
@click.argument("engine")
@click.argument("data")
@click.option("--filter", "-f")
def make(engine, data, filter):
    auto_generate(
        engine_config=engine,
        data=data,
        filter_config=filter
    )


if __name__ == "__main__":
    cli()