from flask import Blueprint, render_template, request
from worf.api.decorators import authorized
from worf.models import User
from worf.settings import settings
import os

main = Blueprint(
    "worf",
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
    static_folder=os.path.join(os.path.dirname(__file__), "static"),
    static_url_path="/static",
)


@main.route("/")
def mainpage():
    return render_template("users.html", user={"name": "andreas"})


@main.route("/users")
@authorized(superuser=False, redirect_to="worf.login")
def users():
    with settings.session() as session:
        users = session.query(User).all()
        return render_template("users.html", user={"name": "andreas"}, users=users)
