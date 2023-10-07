from fck_aws_sso.authorize_sso import authorize_sso
from fck_aws_sso.io import read_stdin_until_data_is_extracted
import typer
import logging

app = typer.Typer()


@app.command()
def main(headless: bool = True, verbose: bool = False):
    """
    A tool to automate AWS SSO login.
    Example: BROWSER=true aws sso login | fck-aws-sso
    """
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    extracted_url, extracted_code = read_stdin_until_data_is_extracted()
    authorize_sso(extracted_url, extracted_code, headless)


if __name__ == "__main__":
    app()
