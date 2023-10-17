# Copyright 2019 Genymobile
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Cli for subcommand auth
"""

import click

from gmsaas.saas import get_client
from gmsaas.storage import authcache
from gmsaas.adbtunnel import get_adbtunnel
from gmsaas.cli.clioutput import ui


def _logout():
    adbtunnel = get_adbtunnel()
    if adbtunnel.is_ready():
        adbtunnel.stop()
    saas = get_client(authcache.get_email(), authcache.get_password())
    saas.logout()
    authcache.clear()


@click.group()
def auth():
    """
    Authentication commands
    """


@click.command(
    "login", help="Authenticate with your credentials.",
)
@click.argument("email")
@click.argument("password", required=False)
def auth_login(email, password):
    """
    Authenticate with you credentials
    """
    # Note: `short_help` makes help text not being truncated to 45 char, don't remove it.
    if not password:
        password = click.prompt("Password", type=click.STRING, hide_input=True)

    _logout()

    client = get_client(email, password)
    jwt = client.login()

    authcache.set_email(email)
    authcache.set_password(password)
    authcache.set_jwt(jwt)

    ui().auth_login(email, authcache.get_path())


@click.command("whoami", help="Display current authenticated user.")
def auth_whoami():
    """
    Display current authenticated user
    """
    ui().auth_whoami(authcache.get_email(), authcache.get_path())


@click.command("logout", help="Disconnect current user.")
def auth_logout():
    """
    Disconnect current user
    """
    _logout()
    ui().auth_logout()


auth.add_command(auth_login)
auth.add_command(auth_whoami)
auth.add_command(auth_logout)
