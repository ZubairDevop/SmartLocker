# This file contains all administrator routes for the Smart Locker application.
# Admin users can view dashboard statistics, manage replacement requests,
# approve/reject requests, manage laptop models, manage locker cells
# and view users with their assigned laptops.

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.user import User
from app.models.request import Request
from app.models.laptop_model import LaptopModel
from app.forms import LaptopModelForm, LockerCellForm
from datetime import datetime
from app import db
import random
import string
from app.models.locker_cell import LockerCell
from app.constants import (
    REQUEST_PENDING,
    REQUEST_REJECTED,
    REQUEST_READY,
    REQUEST_COMPLETED,
    CELL_AVAILABLE,
    CELL_RESERVED,
    CELL_REPAIR,
    CELL_EMPTY,
    LAPTOP_AVAILABLE,
    LAPTOP_REPAIR,
    ROLE_ADMIN,
    LAPTOP_RETIRED
)

admin = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


@admin.route("/")
@login_required
def dashboard():
    

    if current_user.role != ROLE_ADMIN:
        return "Access denied", 403
# Count request statuses to display on dashboard cards.
    pending_requests = Request.query.filter_by(status=REQUEST_PENDING).count()
    ready_requests = Request.query.filter_by(status=REQUEST_READY).count()
    completed_requests = Request.query.filter_by(status=REQUEST_COMPLETED).count()
# Count locker cell statuses to display on dashboard cards.
    available_cells = LockerCell.query.filter_by(status=CELL_AVAILABLE).count()
    reserved_cells = LockerCell.query.filter_by(status=CELL_RESERVED).count()
    repair_cells = LockerCell.query.filter_by(status=CELL_REPAIR).count()
# # Count laptop model statuses to display on dashboard cards
    available_laptops = LaptopModel.query.filter_by(status=LAPTOP_AVAILABLE).count()
    repair_laptops = LaptopModel.query.filter_by(status=LAPTOP_REPAIR).count()

    return render_template(
        "admin/dashboard.html",
        pending_requests=pending_requests,
        ready_requests=ready_requests,
        completed_requests=completed_requests,
        available_cells=available_cells,
        reserved_cells=reserved_cells,
        repair_cells=repair_cells,
        available_laptops=available_laptops,
        repair_laptops=repair_laptops
    )

# Displays all replacement requests for admin. Requests are sorted by newest first.
@admin.route("/requests")
@login_required
def requests():

    if current_user.role != ROLE_ADMIN:
        return "Access denied", 403

    all_requests = Request.query.order_by(
        Request.request_date.desc()
    ).all()

    return render_template(
        "admin/requests.html",
        requests=all_requests
    )

# Generates a random 6-character alphanumeric collection code.
# This code is used by the user to collect their replacement laptop.
def generate_collection_code():
    characters = string.ascii_uppercase + string.digits
    return "".join(random.choice(characters) for _ in range(6))


# Approves a replacement request.
# Finds an available locker cell matching the requested laptop category,
# reserves the cell, generates a collection code and marks the request as ready.
@admin.route("/requests/<int:request_id>/approve")
@login_required
def approve_request(request_id):

    if current_user.role != ROLE_ADMIN:
        return "Access denied", 403

    request = Request.query.get_or_404(request_id)

    available_cell = LockerCell.query.join(
        LockerCell.laptop
    ).filter(
        LockerCell.status == CELL_AVAILABLE,
        LockerCell.laptop.has(category=request.requested_category)
    ).first()

    if not available_cell:
        flash("No available locker cell found for this laptop category.", "danger")
        return redirect(url_for("admin.requests"))

    request.status = REQUEST_READY
    request.approval_date = datetime.utcnow()
    request.locker_cell_id = available_cell.id
    request.collection_code = generate_collection_code()
    request.collection_viewed = False

    available_cell.status = CELL_RESERVED

    db.session.commit()

    flash("Request approved and locker cell reserved successfully.", "success")

    return redirect(url_for("admin.requests"))

# Rejects a replacement request and updates its status.
@admin.route("/requests/<int:request_id>/reject")
@login_required
def reject_request(request_id):

    if current_user.role != ROLE_ADMIN:
        return "Access denied", 403

    request = Request.query.get_or_404(request_id)

    request.status = REQUEST_REJECTED

    db.session.commit()

    flash("Request rejected successfully.", "info")

    return redirect(url_for("admin.requests"))

# Displays all laptop models available in the system.
@admin.route("/laptops")
@login_required
def laptops():

    if current_user.role != ROLE_ADMIN:
        return "Access denied", 403

    laptops = LaptopModel.query.order_by(
        LaptopModel.manufacturer
    ).all()

    return render_template(
        "admin/laptops.html",
        laptops=laptops
    )

# admin can add new laptop Models
@admin.route("/laptops/add", methods=["GET", "POST"])
@login_required
def add_laptop():

    form = LaptopModelForm()

    if form.validate_on_submit():

        laptop = LaptopModel(
            manufacturer=form.manufacturer.data,
            model=form.model.data,
            category=form.category.data,
            status=LAPTOP_AVAILABLE
        )

        db.session.add(laptop)
        db.session.commit()

        flash("Laptop model added successfully.", "success")

        return redirect(url_for("admin.laptops"))

    return render_template(
        "admin/laptop_form.html",
        form=form,
        title="Add Laptop Model"
    )
# admin can edit existing laptop Models
@admin.route("/laptops/<int:laptop_id>/edit", methods=["GET", "POST"])
@login_required
def edit_laptop(laptop_id):

    if current_user.role != ROLE_ADMIN:
        return "Access denied", 403

    laptop = LaptopModel.query.get_or_404(laptop_id)

    form = LaptopModelForm(obj=laptop)

    if form.validate_on_submit():

        laptop.manufacturer = form.manufacturer.data
        laptop.model = form.model.data
        laptop.category = form.category.data

        db.session.commit()

        flash("Laptop model updated successfully.", "success")

        return redirect(url_for("admin.laptops"))

    return render_template(
        "admin/laptop_form.html",
        form=form,
        title="Edit Laptop Model"
    )

# Retires a laptop model instead of deleting it.
@admin.route("/laptops/<int:laptop_id>/retire")
@login_required
def retire_laptop(laptop_id):

    if current_user.role != ROLE_ADMIN:
        return "Access denied", 403

    laptop = LaptopModel.query.get_or_404(laptop_id)

    laptop.status = LAPTOP_RETIRED

    db.session.commit()

    flash("Laptop model retired successfully.", "warning")

    return redirect(url_for("admin.laptops"))

# Displays all Smart Locker cells and their current laptop/status.
@admin.route("/locker")
@login_required
def locker():

    if current_user.role != ROLE_ADMIN:
        return "Access denied", 403

    cells = LockerCell.query.order_by(
        LockerCell.cell_number
    ).all()

    return render_template(
        "admin/locker.html",
        cells=cells
    )


# admin can edit locker cells.
# Admins can change the assigned laptop or set the cell to Empty.
@admin.route("/locker/cell/<int:cell_id>/edit", methods=["GET", "POST"])
@login_required
def edit_locker_cell(cell_id):

    if current_user.role != ROLE_ADMIN:
        return "Access denied", 403

    cell = LockerCell.query.get_or_404(cell_id)

    form = LockerCellForm()

    laptops = LaptopModel.query.filter(
        LaptopModel.status != LAPTOP_RETIRED
    ).all()

    form.laptop_id.choices = [(0, "Empty")] + [
        (laptop.id, f"{laptop.manufacturer} {laptop.model} ({laptop.category})")
        for laptop in laptops
    ]

    if request.method == "GET":
        form.laptop_id.data = cell.laptop_id or 0
        form.status.data = cell.status

    if form.validate_on_submit():

        if form.laptop_id.data == 0:
            cell.laptop_id = None
            cell.status = CELL_EMPTY
        else:
            cell.laptop_id = form.laptop_id.data
            cell.status = form.status.data

        db.session.commit()

        flash("Locker cell updated successfully.", "success")

        return redirect(url_for("admin.locker"))

    return render_template(
        "admin/locker_cell_form.html",
        form=form,
        cell=cell
    )

# Displays all users and their currently assigned laptop.
# Sorted by most recently updated users first.
@admin.route("/users")
@login_required
def users():

    if current_user.role != ROLE_ADMIN:
        return "Access denied", 403

    users = User.query.order_by(
        User.updated_at.desc()
    ).all()

    return render_template(
        "admin/users.html",
        users=users
    )