"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Perfect Python Package."""
    print("test")


if __name__ == "__main__":
    main(prog_name="perf-py-pkg")  # pragma: no cover
