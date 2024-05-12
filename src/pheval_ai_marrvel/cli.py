import click

from pheval_ai_marrvel.post_process.post_process import post_process


@click.group()
def main():
    """AI-MARRVEL runner."""


main.add_command(post_process)

if __name__ == "__main__":
    main()
