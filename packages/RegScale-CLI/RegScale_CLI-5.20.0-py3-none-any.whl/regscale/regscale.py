#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Main script for starting RegScale CLI application """

# standard python imports
import os
import sys
from getpass import getpass
from typing import Optional
from urllib.parse import urlparse

import click
from rich.console import Console

from regscale.models.app_models.click import NotRequiredIf
from regscale.models.app_models.click import regscale_id, regscale_module

# Fitz library requires this static directory in the PWD.
if not os.path.exists("./static"):
    os.makedirs("./static")

############################################################
# Internal Integrations
############################################################
import regscale.core.app.internal.healthcheck as hc
import regscale.core.app.internal.login as lg


############################################################
# Versioning
############################################################
from regscale import __version__
from regscale.core.app import create_logger

############################################################
# Application Integrations
############################################################
from regscale.core.app.application import Application
from regscale.core.app.internal.admin_actions import actions
from regscale.core.app.internal.assessments_editor import assessments
from regscale.core.app.internal.catalog import catalog
from regscale.core.app.internal.comparison import compare
from regscale.core.app.internal.control_editor import control_editor
from regscale.core.app.internal.encrypt import IOA21H98, JH0847, YO9322
from regscale.core.app.internal.evidence import evidence
from regscale.core.app.internal.migrations import migrations
from regscale.core.app.internal.poam_editor import issues
from regscale.core.app.utils.regscale_utils import update_regscale_config
from regscale.core.app.internal.file_uploads import file_upload

############################################################
# Commercial Integrations
############################################################
from regscale.integrations.commercial.ad import ad
from regscale.integrations.commercial.aws import aws
from regscale.integrations.commercial.azure import azure
from regscale.integrations.commercial.crowdstrike import crowdstrike
from regscale.integrations.commercial.defender import defender
from regscale.integrations.commercial.dependabot import dependabot
from regscale.integrations.commercial.gitlab import gitlab
from regscale.integrations.commercial.jira import jira
from regscale.integrations.commercial.okta import okta
from regscale.integrations.commercial.qualys import qualys
from regscale.integrations.commercial.salesforce import salesforce
from regscale.integrations.commercial.servicenow import servicenow
from regscale.integrations.commercial.sonarcloud import sonarcloud
from regscale.integrations.commercial.stig import stig
from regscale.integrations.commercial.tenable import tenable
from regscale.integrations.commercial.wiz import wiz

############################################################
# Public Integrations
############################################################
from regscale.core.app.public.otx import alienvault
from regscale.integrations.public.cisa import cisa
from regscale.core.app.public.emass import emass
from regscale.core.app.public.fedramp.fedramp import fedramp
from regscale.core.app.public.nist_catalog import nist
from regscale.core.app.public.oscal import oscal

############################################################
# CLI Command Definitions
############################################################

console = Console()

app = Application()

logger = create_logger()


@click.group()
def cli() -> click.Group:
    """
    Welcome to the RegScale CLI client app!
    """


# About function
@cli.command()
def about():
    """Provides information about the CLI and its current version."""
    banner()
    about_display()


def about_display():
    """Provides information about the CLI and its current version."""
    console.print(f"[red]RegScale[/red] CLI Version: {__version__}")
    console.print("Author: J. Travis Howerton (thowerton@regscale.com)")
    console.print("Copyright: RegScale Incorporated")
    console.print("Pre-Requisite: Python 3.9 or later")
    console.print("Website: https://www.regscale.com")
    console.print("Read the CLI Docs: https://regscale.readme.io/docs/overview")
    console.print(
        "\n[red]DISCLAIMER: RegScale does not conduct any form of security scanning for data imported by the customer. "
        + "It is the customer's responsibility to ensure that data imported into the platform using "
        + "the Command Line Interface meets industry standard, minimum security screening requirements. "
        + "RegScale has no liability for failing to scan any such data or for any data imported by "
        + "the customer that fails to meet such requirements.[red]\n"
    )


def banner():
    """RegScale logo banner"""
    txt = """
\t[#10c4d3] .';;;;;;;;;;;;;[#14bfc7];;;;;;;;;;;;,'..
\t[#10c4d3].:llllllllllllll[#14bfc7]lllllllllllllllc:'.
\t[#10c4d3].cliclicliclicli[#14bfc7]clicliclicliclooool;.
\t[#10c4d3].cliclic###################;:looooooc'
\t[#05d1b7].clicli,                     [#15cfec].;loooool'
\t[#05d1b7].clicli,                       [#18a8e9].:oolloc.
\t[#05d1b7].clicli,               [#ef7f2e].,cli,.  [#18a8e9].clllll,
\t[#05d1b7].clicli.             [#ef7f2e].,oxxxxd;  [#158fd0].:lllll;
\t[#05d1b7] ..cli.            [#f68d1f]';cdxxxxxo,  [#18a8e9].cllllc,
\t                 [#f68d1f].:odddddddc.  [#1b97d5] .;ccccc:.
\t[#ffc42a]  ..'.         [#f68d1f].;ldddddddl'  [#0c8cd7].':ccccc:.
\t[#ffc42a] ;xOOkl.      [#e9512b]'coddddddl,.  [#0c8cd7].;::::::;.
\t[#ffc42a]'x0000O:    [#e9512b].:oooooool;.  [#0c8cd7].,::::::;'.
\t[#ffc42a]'xO00OO:  [#e9512b].;loooooo:,.  [#0c8cd7].';::;::;'.
\t[#ff9d20]'xOOOOOc[#ba1d49].'cllllllc'    [#0c83c8].,;;;;;;,.
\t[#ff9d20]'xOOOOOo[#ba1d49]:clllllc'.     [#0c83c8]';;;;;;'.
\t[#ff9d20]'xOOOOOd[#ba1d49]ccccc:,.       [#1a4ea4].',,,,'''.
\t[#ff9d20]'dOOOOkd[#ba1d49]c:::,.           [#1a4ea4]..''''''..
\t[#f68d1f]'dkkkkko[#ba1d49]:;,.               [#1a4ea4].''''','..
\t[#f68d1f]'dkkkkkl[#ba1d49],.                   [#0866b4].''',,,'.
\t[#f68d1f].lkkkkx;[#ba1d49].                     [#0866b4]..',,,,.
\t[#f68d1f] .;cc:'                         [#0866b4].....
 """
    console.print(txt)


@cli.command("version")
def version():
    """Display the version information and exit."""
    print(__version__)


@cli.command(name="change_passkey")
def change_passkey():
    """Change your encryption/decryption passkey."""
    YO9322()
    sys.exit()


@cli.command()
@click.option(
    "--file", hide_input=False, help="File to encrypt.", prompt=True, required=True
)
def encrypt(file):
    """Encrypts .txt, .yaml, .json, & .csv files."""
    if file:
        JH0847(file)
        sys.exit()


@cli.command()
@click.option(
    "--file", hide_input=False, help="File to decrypt.", prompt=True, required=True
)
def decrypt(file):
    """Decrypts .txt, .yaml, .json, & .csv files."""
    if file:
        IOA21H98(file)
        sys.exit()


# Update config parameter
@cli.command()
@click.option(
    "--param",
    hide_input=False,
    help="CLI config parameter name.",
    prompt=True,
    required=True,
    type=click.STRING,
)
@click.option(
    "--val",
    hide_input=True,
    help="CLI config parameter value.",
    type=click.STRING,  # default is string even if entering an integer
    prompt=True,
    required=True,
)
def config(param, val, app=app):
    """Updates init.yaml config parameter with value"""
    # check if key provided exists in init.yaml or the app.template before adding it
    if param in app.config or param in app.template:
        # check the datatype provided vs what is expected
        if isinstance(val, (type(app.config[param]), type(app.template[param]))):
            # update init file from login
            result_msg = update_regscale_config(param, val, app=app)
            # print the result
            logger.info(result_msg)
        else:
            # try to convert val entry to an int
            try:
                int_val = int(val)
                # update init file from login
                result_msg = update_regscale_config(param, int_val, app=app)
                # print the result
                logger.info(result_msg)
            except ValueError:
                logger.error(
                    "%s needs a %s value, but a %s was provided.",
                    param,
                    type(app.template[param]),
                    type(val),
                )
                sys.exit(1)
    else:
        message = (
            f"{param} is not required for RegScale CLI and was not added to init.yaml."
        )
        message += "If you believe this is incorrect, please add the key and value to init.yaml manually."
        logger.error(message)


# Log into RegScale to get a token
@cli.command(name="validate_token")
def validate_token():
    """Check to see if token is valid."""
    if lg.is_valid(app=app):
        logger.info("RegScale token is valid.")
        sys.exit(0)
    else:
        logger.warning("RegScale token is invalid, please login.")
        sys.exit(1)


@cli.command()
@click.option(
    "--username",
    hide_input=False,
    help="RegScale User Name.",
    type=click.STRING,
    default=os.getenv("REGSCALE_USER"),
    cls=NotRequiredIf,
    not_required_if=["token"],
)
@click.option(
    "--password",
    hide_input=True,
    help="RegScale password.",
    default=os.getenv("REGSCALE_PASSWORD"),
    cls=NotRequiredIf,
    not_required_if=["token"],
)
@click.option(
    "--token",
    hide_input=True,
    help="RegScale JWT Token.",
    prompt=False,
    default=None,
    type=click.STRING,
    cls=NotRequiredIf,
    not_required_if=["username", "password", "mfa_token"],
)
@click.option(
    "--domain",
    hide_input=True,
    help="RegScale Domain (e.g. https://regscale.yourcompany.com)",
    prompt=False,
    required=False,
    default=os.getenv("REGSCALE_DOMAIN"),
    type=click.STRING,
)
@click.option(
    "--mfa_token",
    hide_input=True,
    help="RegScale MFA Token.",
    type=click.STRING,
    cls=NotRequiredIf,
    not_required_if=["token"],
)
def login(
    username: Optional[str],
    password: Optional[str],
    token: Optional[str] = None,
    domain: Optional[str] = None,
    mfa_token: Optional[str] = None,
):
    """Logs the user into their RegScale instance."""
    if token:
        lg.login(token=token, host=domain, app=app)
        sys.exit(0)
    if not username:
        username = click.prompt("Username", type=str)
    if not password:
        password = click.prompt("Password", type=str, hide_input=True)
    if mfa_token:
        lg.login(
            str_user=username,
            str_password=password,
            mfa_token=mfa_token,
            app=app,
            host=domain,
        )
    else:
        lg.login(str_user=username, str_password=password, app=app, host=domain)


# Check the health of the RegScale Application
@cli.command()
def healthcheck():
    """Monitoring tool to check the health of the RegScale instance."""
    hc.status()


@cli.command()
@click.option(
    "--domain",
    type=click.STRING,
    help="RegScale domain URL to skip domain prompt.",
    prompt=False,
    default=os.getenv("REGSCALE_DOMAIN"),
    required=False,
)
@click.option(
    "--username",
    type=click.STRING,
    help="RegScale User Name to skip login prompt.",
    hide_input=False,
    prompt=False,
    required=False,
    default=os.getenv("REGSCALE_USER"),
)
@click.option(
    "--password",
    type=click.STRING,
    help="RegScale password to skip login prompt.",
    hide_input=True,
    default=os.getenv("REGSCALE_PASSWORD"),
    prompt=False,
    required=False,
)
@click.option(
    "--mfa_token",
    type=click.STRING,
    help="MFA Token used to log into RegScale.",
    default="",
    prompt=False,
    required=False,
)
@click.option(
    "--user_id",
    type=click.STRING,
    help="RegScale User ID to skip login prompt.",
    hide_input=False,
    prompt=False,
    required=False,
    default=os.getenv("REGSCALE_USER_ID"),
)
@click.option(
    "--token",
    type=click.STRING,
    help="RegScale JWT Token to skip login prompt.",
    hide_input=True,
    prompt=False,
    required=False,
    default=os.getenv("REGSCALE_TOKEN"),
)
@click.option(
    "--skip-prompts",
    is_flag=True,
    help="Skip domain and login prompts.",
)
def init(
    domain: str = None,
    username: str = None,
    password: str = None,
    user_id: str = None,
    token: str = None,
    mfa_token: Optional[str] = "",
    skip_prompts: Optional[bool] = False,
):
    """Initialize RegScale CLI environment"""
    console.print("Initializing your RegScale CLI environment...")
    # skip prompts when no-prompts flag sent
    if skip_prompts:
        os.remove("init.yaml")
        Application()
        domain_to_use = domain or os.getenv("REGSCALE_DOMAIN")
        if not domain_to_use:
            console.print(
                "[red]You must pass a domain or set the REGSCALE_DOMAIN environment variable"
            )
            sys.exit(1)
        app.config["domain"] = domain_to_use
        if user_id:
            app.config["userId"] = user_id
        if token:
            app.config["token"] = token
        app.save_config(conf=app.config)
        banner()
        about_display()
        console.print(
            f'Successfully initialized with Domain [green]{app.config["domain"]}.'
        )
        console.print("logging in . . .")
        lg.login(token=token, host=domain_to_use, app=app)
        console.print("Logged in successfully.")
        return None

    domain_prompt = "n"
    # see if user used the --domain flag
    if not domain:
        domain_prompt = (
            input(
                f"Would you like to change your RegScale domain from {app.config['domain']}? (Y/n): "
            )
            or "y"
        )

    # if the user used --domain or entered y to change their domain when prompted
    if domain or domain_prompt[0].lower() == "y":
        # make sure --domain wasn't used & input yes to change their domain
        if not skip_prompts and not domain and domain_prompt[0].lower() == "y":
            # prompt user for the new domain
            domain = input(
                "\nPlease enter your RegScale domain.\nExample: https://mydomain.regscale.com/\nDomain: "
            )

        # parse the domain entry for a URL
        result = urlparse(domain)

        # check if the domain provided is a valid URL
        if all([result.scheme, result.netloc]):
            # update the domain in init.yaml with the user's provided domain
            update_regscale_config(str_param="domain", val=domain, app=app)
            logger.info("Valid URL provided, init.yaml has been updated.")
        else:
            logger.error("Invalid URL provided, init.yaml was not updated.")
    # make sure --username and --password weren't used before asking if user wants to log in
    if not username and not password:
        # prompt the user if they would like to log in to their RegScale instance
        login_prompt = (
            input("Would you like to log in to your RegScale instance? (Y/n): ") or "y"
        )
    # see if user used --username, --password or entered yes to log in to RegScale
    if username or password or login_prompt[0].lower() == "y":
        # if no username was provided, ask for one
        if not username:
            username = input("Please enter your username: ")
        # if no password was provided, ask for one
        if not password:
            # hide the password entry with getpass()
            password = getpass("Please enter your password: ")
        # try to log in with provided username and password
        lg.login(username, password, host=domain, app=app, mfa_token=mfa_token)
    banner()
    about_display()


@cli.command(name="upload_file")
@regscale_id()
@regscale_module()
@click.option(
    "--file_path",
    "-f",
    type=click.Path(exists=True),
    help="The path to the file to upload to RegScale.",
    prompt="File to upload to RegScale.",
    required=True,
)
def upload_file(regscale_id, regscale_module, file_path):
    """Upload a file from your local machine to a record in RegScale."""
    file_upload(regscale_id, regscale_module, file_path)


############################################################
# Add Application Integrations
############################################################
cli.add_command(actions)  # add Reminder Functionality
cli.add_command(assessments)  # add Assessments Editor Feature
cli.add_command(catalog)  # add Catalog Management Feature
cli.add_command(compare)  # add Comparison support
cli.add_command(control_editor)  # add Control Editor Feature
cli.add_command(evidence)  # add Evidence Feature
cli.add_command(migrations)  # add data migration support
cli.add_command(issues)  # add POAM(Issues) Editor Feature

############################################################
# Add Commercial Integrations
############################################################
cli.add_command(ad)  # add Azure Active Directory (AD) support
cli.add_command(aws)  # add AWS support
cli.add_command(azure)  # add Azure Integration
cli.add_command(defender)  # add Microsoft Defender Functionality
cli.add_command(dependabot)  # add Dependabot Integration
cli.add_command(gitlab)  # add GitLab
cli.add_command(jira)  # add JIRA support
cli.add_command(okta)  # add Okta Support
cli.add_command(qualys)  # add Qualys Functionality
cli.add_command(salesforce)  # add Salesforce support
cli.add_command(servicenow)  # add ServiceNow support
cli.add_command(sonarcloud)  # add SonarCloud Integration
cli.add_command(stig)  # add STIG support
cli.add_command(tenable)  # add Tenable support
cli.add_command(wiz)  # add Wiz support

############################################################
# Add Public Integrations
############################################################
cli.add_command(alienvault)  # add Alienvault OTX integration
cli.add_command(cisa)  # add CISA support
cli.add_command(emass)  # add eMASS support
cli.add_command(fedramp)  # add FedRAMP support
cli.add_command(nist)  # add Nist_Catalog support
cli.add_command(oscal)  # add OSCAL support

# add CrowdStrike
cli.add_command(crowdstrike)

# start function for the CLI
if __name__ == "__main__":
    cli()
