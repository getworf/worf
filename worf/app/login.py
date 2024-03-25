from worf.utils.forms import Form, Field
from worf.utils.forms.validators import String, Required, EMail, Length
from worf.api.v1.resources.user.login import generate_access_token
from worf.settings import settings
from worf.api.decorators import AuthError
from .main import main
from flask import request, render_template, redirect, url_for


class LoginForm(Form):
    email = Field([Required(), EMail()])
    password = Field([Required(), String(), Length(min=8)])


@main.route("/login", methods=["GET", "POST"])
def login():
    def error(reason):
        return render_template("login.html", reason=reason)

    if request.method == "POST":
        login_form = LoginForm(request.form)
        if not login_form.validate():
            return render_template(
                "login.html", errors=login_form.errors, form=login_form
            )

        with settings.session() as session:
            providers = settings.providers.get("login.password")
            if not providers:
                return error("Cannot log in with password")

            # we initialize the login provider
            provider = providers[0](session)

            result = provider.login(login_form.valid_data)

            if result.get("error"):
                return error("Invalid username or password")

            token = generate_access_token(
                result["user"],
                "password",
                session,
                trusted=False,
            )

            resp = redirect(url_for("worf.mainpage"))
            resp.set_cookie("access_token", token.token)
            return resp

    reason = request.args.get("reason")
    reason_str = ""

    if reason:
        match AuthError[reason]:
            case AuthError.NoToken:
                reason_str = "Please log in to access this content"

    return render_template("login.html", reason=reason_str, errors={})
