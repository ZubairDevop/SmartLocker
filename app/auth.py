# Import Flask utilities used for routing, templates,
# redirects and user notifications.
from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash

# Flask-Login functions used for authentication and session management.
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required

# Import login form and user model.
from app.forms import LoginForm
from app.models.user import User

# Import role constants used for role-based redirection.
from app.constants import ROLE_ADMIN
from app.constants import ROLE_USER

# Authentication blueprint. Handles login and logout functionality.
auth = Blueprint(
    "auth",
    __name__
)

            
# Login route handles both displaying the login page GET and processing login requests POST
@auth.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        # Normalise email by removing spaces and converting to lowercase.
        email = form.email.data.lower().strip()
        # Search for user account exists matching the email address.
        user = User.query.filter_by(
            email=email
        ).first()

        # Verify that the user exists and the password hash matches.
        if user and user.check_password(form.password.data):

            # create user session after authentication
            login_user(user)

            flash(
                f"Welcome {user.first_name}!",
                "success"
            )

            # Role Based Access Control (RBAC)
            # Administrators will be routed to admin dashboard and Standard users to user dashboard
            if user.role == ROLE_ADMIN:
                return redirect(url_for("admin.dashboard"))

            return redirect(url_for("user.dashboard"))

        
        form.password.errors.append(
            "Invalid email or password."
        )

    return render_template(
        "login.html",
        form=form
    )
# logout user and ends session, while flashing message for log out
@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "You have been logged out.",
        "info"
    )

    return redirect(url_for("main.home"))