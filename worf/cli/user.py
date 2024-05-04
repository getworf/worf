import click

from worf.settings import settings
from worf.models import User, AccessToken, Tenant


@click.group("user")
def user():
    """
    User-related commands.
    """
    pass


@user.command("create")
@click.argument("tenant_name")
@click.argument("email")
@click.option("--superuser", is_flag=True)
def create_user(tenant_name, email, superuser):
    """
    Create a user
    """
    with settings.session() as session:
        tenant = Tenant.get_by_name(session, tenant_name)
        if not tenant:
            click.echo("Invalid tenant")
        if User.get_by_email(session, tenant, email):
            click.echo("User already exists.")
            return
        user = User(tenant=tenant, email=email, superuser=superuser)
        session.add(user)


@user.command("update")
@click.argument("tenant_name")
@click.argument("email")
@click.option("--superuser", is_flag=True)
def update(tenant_name, email, superuser):
    """
    Update a user
    """
    with settings.session() as session:
        tenant = Tenant.get_by_name(session, tenant_name)
        if not tenant:
            click.echo("Invalid tenant")
        user = User.get_by_email(session, tenant, email)
        if not user:
            click.echo("User does not exist.")
            return
        click.echo("Setting superuser to {}".format(superuser))
        user.superuser = superuser
        session.add(user)


@user.command("token")
@click.argument("tenant_name")
@click.argument("email")
@click.option("--trusted", is_flag=True)
def token(tenant_name, email, trusted):
    """
    Return an access token for the user
    """
    with settings.session() as session:
        tenant = Tenant.get_by_name(session, tenant_name)
        if not tenant:
            click.echo("Invalid tenant")
        user = User.get_by_email(session, tenant, email)
        if not user:
            click.echo("User does not exist.")
            return
        access_token = AccessToken(
            user_id=user.id,
            renews_when_used=True,
            scopes="admin",
        )
        session.add(access_token)
    click.echo(f"Token: {access_token.token}")
