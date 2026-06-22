from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash

from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required

from app.forms import LoginForm
from app.models.user import User

from app.constants import ROLE_ADMIN
from app.constants import ROLE_USER

auth = Blueprint(
    "auth",
    __name__
)

            





@auth.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        email = form.email.data.lower().strip()

        user = User.query.filter_by(
            email=email
        ).first()

        if user and user.check_password(form.password.data):

            login_user(user)

            flash(
                f"Welcome {user.first_name}!",
                "success"
            )

            if user.role == ROLE_ADMIN:
                return redirect(url_for("admin.dashboard"))

            return redirect(url_for("user.dashboard"))

        flash(
            "Invalid email or password.",
            "danger"
        )

    return render_template(
        "login.html",
        form=form
    )

@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "You have been logged out.",
        "info"
    )

    return redirect(url_for("main.home"))