# flask_wtf supports CSRF protection along with with wtforms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, InputRequired, Email, ValidationError
from app.constants import (
    CATEGORY_STANDARD,
    CATEGORY_EXECUTIVE,
    PRIORITY_LOW,
    PRIORITY_MEDIUM,
    PRIORITY_HIGH
)

# validation stuctured so only cgi email address is accepted
def validate_cgi_email(form, field):

    email = field.data.lower().strip()

    if not email.endswith("@cgi.com"):

        raise ValidationError(
            "Please use your CGI email address."
        )
    
# login form, email must be in valid format
class LoginForm(FlaskForm):

    email = StringField(
        "Email Address",
        validators=[
            DataRequired(),
            Email(),
            validate_cgi_email
        ]
    )

# password autnetication
    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )

    submit = SubmitField("Login")

# a class is created to to support laptop replacement. user can only select like for like laptop. 
class ReplacementRequestForm(FlaskForm):

    requested_category = SelectField(
        "Replacement Laptop Category",
        choices=[
            (CATEGORY_STANDARD, "Standard Laptop"),
            (CATEGORY_EXECUTIVE, "Executive Laptop")
        ],
        validators=[DataRequired()]
    )

# description length restricted so only can add useful information
    issue_description = TextAreaField(
        "Describe the laptop issue",
        validators=[
            DataRequired(),
            Length(min=10, max=500)
        ]
    )

# user select priority
    priority = SelectField(
        "Priority",
        choices=[
            (PRIORITY_LOW, "Low"),
            (PRIORITY_MEDIUM, "Medium"),
            (PRIORITY_HIGH, "High")
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField("Submit Request")

# form for admin to add or edit laptop model
class LaptopModelForm(FlaskForm):

    manufacturer = StringField(
        "Manufacturer",
        validators=[DataRequired()]
    )

    model = StringField(
        "Model",
        validators=[DataRequired()]
    )

    category = SelectField(
        "Category",
        choices=[
            (CATEGORY_STANDARD, "Standard"),
            (CATEGORY_EXECUTIVE, "Executive")
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField("Save")

# admin form to manage locker cell
class LockerCellForm(FlaskForm):

    laptop_id = SelectField(
        "Laptop Model",
        coerce=int,
        validators=[InputRequired()]
    )

# admin to update locker cell status
    status = SelectField(
        "Cell Status",
        choices=[
            ("Available", "Available"),
            ("Reserved", "Reserved"),
            ("Repair", "Repair"),
            ("Empty", "Empty")
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField("Save")


