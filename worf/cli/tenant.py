import click

from worf.settings import settings
from worf.models import Tenant


@click.group("tenant")
def tenant():
    """
    Tenant-related commands.
    """
    pass


@tenant.command("create")
@click.argument("name")
def create_tenant(name):
    """
    Create a tenant
    """
    with settings.session() as session:
        if Tenant.get_by_name(session, name):
            click.echo("Tenant already exists.")
            return
        tenant = Tenant(name=name)
        session.add(tenant)
