from flask import Blueprint, render_template

# Creating main blueprint used for public application route
main = Blueprint("main", __name__)

# Home page route. Displays the Smart Locker landing page.
@main.route("/")
def home():
    return render_template("index.html")