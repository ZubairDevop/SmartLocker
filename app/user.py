# Import Flask tools for routing, rendering templates, messages and redirects
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models.request import Request
from app import db
from app.forms import ReplacementRequestForm
from app.constants import (
    REQUEST_PENDING,
    REQUEST_APPROVED,
    REQUEST_READY,
    REQUEST_COMPLETED,
    CELL_REPAIR
)
# Creating user blueprint. for all routes in this file to start with /user.
user = Blueprint(
    "user",
    __name__,
    url_prefix="/user"
)

# User dashboard route. Displays the logged-in user's active request, if one exists.
# Only pending, approved and ready requests are active requests.
@user.route("/")
@login_required
def dashboard():
    
    # this code will search for an active request belonging to the logged-in user.
    # Completed, rejected and cancelled requests are excluded.
    active_request = Request.query.filter(
        Request.user_id == current_user.id,
        Request.status.in_([
            REQUEST_PENDING,
            REQUEST_APPROVED,
            REQUEST_READY
        ])
    ).first()

    return render_template(
        "user/dashboard.html",
        active_request=active_request
    )

# this code will allow a logged-in user to create a replacement laptop request.
# Users can only request a laptop from their assigned category.
@user.route("/request", methods=["GET", "POST"])
@login_required
def create_request():

    form = ReplacementRequestForm()

    # Pre-select the request category based on the user's assigned laptop category.
    form.requested_category.data = current_user.assigned_category

    active_request = Request.query.filter(
        Request.user_id == current_user.id,
        Request.status.in_([
            REQUEST_PENDING,
            REQUEST_APPROVED,
            REQUEST_READY
        ])
    ).first()

    # Prevent the user from creating more than one active request at a time.
    if active_request:
        flash("You already have an active replacement request.", "warning")
        return redirect(url_for("user.dashboard"))

    if form.validate_on_submit():

        # Enforce like-for-like replacement rule.
        # Standard users can only request Standard laptops.
        # Executive users can only request Executive laptops.
        if form.requested_category.data != current_user.assigned_category:
            flash("You can only choose like for like laptop.", "danger")
            return redirect(url_for("user.create_request"))

        # Create a new replacement request and store it as Pending.
        new_request = Request(
            user_id=current_user.id,
            requested_category=current_user.assigned_category,
            issue_description=form.issue_description.data,
            priority=form.priority.data,
            status=REQUEST_PENDING
        )

        db.session.add(new_request)
        db.session.commit()

        flash("Replacement request submitted successfully.", "success")
        return redirect(url_for("user.dashboard"))

    return render_template(
        "user/create_request.html",
        form=form
    )

# Displays the one-time collection code for an approved request.
# Once viewed, the request is completed and the locker cell moves to Repair.
@user.route("/collection-code/<int:request_id>")
@login_required
def view_collection_code(request_id):

    request = Request.query.get_or_404(request_id)

    # Ensure users can only access their own collection code.
    if request.user_id != current_user.id:
        return "Access denied", 403

    # Collection code is only available when the request is ready for collection.
    if request.status != REQUEST_READY:
        flash("Collection code is not available for this request.", "warning")
        return redirect(url_for("user.dashboard"))

    # Prevent the one-time collection code from being viewed again.
    if request.collection_viewed:
        flash("Collection code has already been viewed.", "danger")
        return redirect(url_for("user.dashboard"))

    collection_code = request.collection_code
    cell_number = request.locker_cell.cell_number

    replacement_laptop = request.locker_cell.laptop
    faulty_laptop_id = current_user.current_laptop_id

    request.collection_viewed = True
    request.status = REQUEST_COMPLETED

    # User now receives the replacement laptop
    current_user.current_laptop_id = replacement_laptop.id

    # Faulty laptop is returned into the locker cell
    request.locker_cell.laptop_id = faulty_laptop_id

    # Cell now contains faulty laptop and should be repaired
    request.locker_cell.status = CELL_REPAIR

    db.session.commit()


    return render_template(
        "user/collection_code.html",
        collection_code=collection_code,
        cell_number=cell_number,
        laptop=replacement_laptop
    )