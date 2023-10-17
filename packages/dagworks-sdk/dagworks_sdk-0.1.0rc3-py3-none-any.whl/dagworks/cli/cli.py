# Copyright (C) 2023-Present DAGWorks Inc.
#
# For full terms email support@dagworks.io.
#
# This software and associated documentation files (the "Software") may only be
# used in production, if you (and any entity that you represent) have agreed to,
# and are in compliance with, the DAGWorks Enterprise Terms of Service, available
# via email (support@dagworks.io) (the "Enterprise Terms"), or other
# agreement governing the use of the Software, as agreed by you and DAGWorks,
# and otherwise have a valid DAGWorks Enterprise license for the
# correct number of seats and usage volume.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os

import click

from dagworks.cli import initialize


@click.group()
def cli():
    pass


@click.command()
@click.option("--api-key", "-k", required=True, type=str)
@click.option("--username", "-u", required=True, type=str)
@click.option("--project-id", "-p", required=True, type=int)
@click.option("--template", "-t", required=False, type=click.Choice(initialize.TEMPLATES))
@click.option("--location", "-l", type=click.Path(exists=False, dir_okay=True), default=None)
def init(api_key: str, username: str, project_id: int, template: str, location: str):
    if location is None:
        # If location is none we default to, say, ./hello_world
        location = os.path.join(os.getcwd(), template)
    initialize.generate_template(
        username=username,
        api_key=api_key,
        project_id=project_id,
        template=template,
        copy_to_location=location,
    )


cli.add_command(init)

if __name__ == "__main__":
    cli()
