import click
from click.testing import CliRunner

@click.command()
def hello():
    click.echo("STDOUT")
    click.secho("STDERR", err=True)

def test():
    runner = CliRunner()
    result = runner.invoke(hello)
    print(f"STDOUT in result.output: {'STDOUT' in result.output}")
    print(f"STDERR in result.output: {'STDERR' in result.output}")
    print(f"result.stderr: {result.stderr}")

if __name__ == '__main__':
    test()
