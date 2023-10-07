from .cli_utils import (kc_admin_command,
                        platforms,
                        with_cache,
                        detect_branch)

from . import keycloak
from . import poolparty
from . import jenkins
from . import github
from . import graphsearch

import click
import tempfile
import time
import math

from pathlib import Path

from loguru import logger


@click.group()
def cli():
    """The venerable P3D command line utils"""
    ...

@cli.group()
def jk():
    """Jenkins commands"""
    ...

@cli.group()
def pp():
    """PoolParty commands"""
    ...

@cli.group()
def kc():
    """Keycloak commands"""
    ...

@cli.group()
def gh():
    """GitHub commands"""
    ...

@cli.group()
def gs():
    """GraphSearch commands"""
    ...


@kc.command()
@click.argument("json", type=click.File('r'))
@click.pass_context
@kc_admin_command
def add_mappers(ctx, json):
    """Add mappers to Keycloak IdP from realm export"""
    kc = keycloak.Keycloak(ctx.obj['server'], ctx.obj['username'], ctx.obj['password'], ctx.obj['user_realm_name'], ctx.obj['realm_name'])
    kc.import_mappers(json)


@gs.command()
@click.option('--amount', prompt=True, type=int, default=5, help='The number of documents to be created in an existing searchspace.')
@click.option("--url", default="http://localhost:8081", prompt=True, help="The url to PoolParty without tailing slash, e.g. http://localhost:8081")
@click.option("--searchspace-id", prompt=True, help="The searchspaceid to use, e.g.: dc17cc35-7ea4-4f09-9764-ae704a6a524e")
@click.option("--username", prompt=True, default="superadmin", help="PoolParty username")
def create_documents(amount: int, url: str, username: str, searchspace_id: str):
    """Create certain amount of documents in ppgs searchSpace
    

    Leave out any of option parameters (--url, --username, --searchspace) to get an
    interactive prompt.
    """
    password = click.prompt('Password', hide_input=True)
    for i in range(amount):
        graphsearch.create_document(url,(username,password),searchspace_id,i)


@pp.command()
@click.argument("clear_text")
@click.option("--password", prompt=True, help="The password used for encryption")
@click.option("--salt", prompt=True, help="The salt used for encryption")
@click.option("--strength", prompt=True, type=click.INT, help="The strength used for encryption")
def encrypt(clear_text: str, password: str, salt: str, strength: int):
    """Encrypt clear text with poolparty encryption

    The settings for PASSWORD, SALT and STRENGTH can usually be found in the
    poolparty.properties file.

    Leave out any of option parameters (--password, --salt, --strengh) to get an
    interactive prompt.
    """
    secret = poolparty.encrypt(clear_text, password, salt, strength)
    print(f"Secret: {secret}")

@pp.command()
@click.argument("secret")
@click.option("--password", prompt=True, help="The password used for decryption")
@click.option("--salt", prompt=True, help="The salt used for decryption")
@click.option("--strength", prompt=True, type=click.INT, help="The strength used for decryption")
def decrypt(secret: str, password: str, salt: str, strength: int):
    """Decrypt secret text with poolparty encryption

    The settings for PASSWORD, SALT and STRENGTH can usually be found in the
    poolparty.properties file.

    Leave out any of the option parameters (--password, --salt, --strengh) to get an interactive prompt.
    """
    clear = poolparty.decrypt(secret, password, salt, strength)
    print(f"Clear: {clear}")

@pp.command()
@click.option("--path", type=click.Path(exists=True, file_okay=False, writable=True))
@platforms(["linux"])
def install_snapshot(path: Path):
    """Download and invoke the snapshot installer

    Specify `--path` to download the installer to a specific folder. Otherwise,
    the installer will be installed in a temporary directory.

    This command is restricted to Linux for now.
    """

    if not path:
        path = Path(tempfile.gettempdir())

    poolparty.install_snapshot(path)


@pp.command()
@click.option("--port", type=click.INT, default=5000, help="The port to run the server on [default: 5000]")
def mock_server(port: int):
    """Runs a mock server for testing and debugging external integrations

    PoolParty provides several integrations with external APIs/services (cf.
    Semantic Middleware Configurator). This command starts a mock server for
    debugging/testing such integrations.

    The port on which to run the server can be specified via --port. It defaults
    to 5000.

    # Webhook consumer
    Starts a server and echoes any request (+ auxiliary information) coming in.
    In addition starts a healthcheck endpoint that just always returns `200 OK`.

    The webhook consumer url (to configure in Semantic Middleware Configurator)
    is `http://localhost:5000/hook`.
    """

    poolparty.run_mock_server(port)


@pp.command()
@click.argument("key", type=click.STRING)
@click.argument("license", type=click.File('r'))
def decrypt_license(key, license):
    """Decrypts a PoolParty license with the PoolParty standard decryption and the given encryption key

    KEY must be the base64 encoded encryption key for PoolParty licenses
    LICENSE is the path to an encrypted license file usually ending in .key
    """

    print(poolparty.decrypt_license(license, key))


@pp.command()
@click.argument("key", type=click.STRING)
@click.argument("license", type=click.File('r'))
def encrypt_license(key, license):
    """Encrypts PoolParty license data with the PoolParty standard encryption and the given encryption key

    KEY must be the base64 encoded encryption key for PoolParty licenses
    LICENSE path to the license data that shall be encrypted as PoolParty license file
    """

    print(poolparty.encrypt_license(license, key))


@jk.command()
@click.option("--branch", help="The branch to build")
@click.option('--no-autodetect', type=click.BOOL, is_flag=True, default=False, help="Disable autodetection of branch in a git repository")
@click.option('--api-user', type=click.STRING, help="Jenkins API user (your username)")
@click.option('--api-key', type=click.STRING, help="Jenkins API key (generate in Jenkins)")
def build(branch: str, no_autodetect: bool, api_key: str, api_user: str):
    """Run the PoolParty build

    Per default (and outside a git repository) builds the `develop` branch of
    PoolParty.

    When inside a git repository `p3do` will automatically detect the current
    branch and build it. This behavior can be disabled with --no-autodetect.

    The branch to build can be specified via --branch (note that this implies
    --no-autodetect inside a git repository).
    """

    api_key = with_cache(api_key, "jk_key", "Jenkins API Key")
    api_user = with_cache(api_user, "jk_user", "Jenkins API User")

    if not branch and no_autodetect:
        branch = "develop"

    branch = branch or detect_branch() or "develop"
    logger.info("Using branch {}", branch)
    url = jenkins.run_build("P3D-BUILD", branch, api_user, api_key)
    print(f"{url}")

@jk.command()
@click.argument("server")
@click.option("--branch", help="The branch to build")
@click.option('--no-autodetect', type=click.BOOL, is_flag=True, default=False, help="Disable autodetection of branch in a git repository")
@click.option('--api-user', type=click.STRING, help="Jenkins API user (your username)")
@click.option('--api-key', type=click.STRING, help="Jenkins API key (generate in Jenkins)")
def deploy(server: str, branch: str, no_autodetect: bool, api_key: str, api_user: str):
    """Run a PoolParty deployment

    Per default (and outside a git repository) deploys the `develop` branch of
    PoolParty.

    When inside a git repository `p3do` will automatically detect the current
    branch and deploy it. This behavior can be disabled with --no-autodetect.

    The branch to deploy can be specified via --branch (note that this implies
    --no-autodetect inside a git repository).

    The <SERVER> argument is mandatory and must be a valid ssh server name.
    PoolParty will be deployed to this server.
    """

    api_key = with_cache(api_key, "jk_key", "Jenkins API Key")
    api_user = with_cache(api_user, "jk_user", "Jenkins API User")

    if not branch and no_autodetect:
        branch = "develop"

    branch = branch or detect_branch() or "develop"
    logger.info("Using branch {}", branch)
    url = jenkins.run_deploy("P3D-Build-Deploy-PoolParty-(parent-pom)", server, branch, api_user, api_key)
    print(f"{url}")

@gh.command()
@click.argument("repository")
@click.argument("ssh-key")
@click.option("--token", help="GitHub access token (generate in GitHub)")
@click.option("--title", help="Title for the deploy key")
@click.option("--write_access", type=click.BOOL, is_flag=True, default=False, help="Allow deploy key write access to the repository")
def deploy_key(repository: str, ssh_key: str, token: str, title: str, write_access: bool):
    """Add a deployment key to a GitHub repository"""

    token = with_cache(token, "gh_key", "GitHub Access Token")

    if not title:
        logger.debug("No title given, inferring title")
        key_sections = ssh_key.split(" ")
        if len(key_sections) >= 3:
            logger.debug("Inferring title from ssh comment section")
            title=key_sections[2]
        else:
            logger.debug("No comment section in ssh key. Using generated title.")
            title = "deploy-key"+str(math.floor(time.time()))

    logger.debug("Cleaning up repository name")
    repository = repository.strip()
    repository = repository.strip('/')
    if not repository.startswith("poolparty-semantic-suite"):
        logger.debug("Repository does not contain `poolparty-semantic-suite` organization. Trying to add organization.")
        repository = "poolparty-semantic-suite/"+repository

    logger.info(f"Creating deploy key {ssh_key} for repository {repository}")
    github.deploy_key(repository, ssh_key, token, title, not write_access)

if __name__ == "__main__":
    cli()
