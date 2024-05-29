from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from models import User, Role, Group, Ticket


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        role_name = request.form["role"]
        group_name = request.form["group"]

        role = Role.query.filter_by(name=role_name).first()
        group = Group.query.filter_by(name=group_name).first()

        user = User()
        user.username = username
        user.email = email
        user.role = role
        user.group = group
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user)
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.role.name == "Admin":
        tickets = Ticket.query.all()
    else:
        tickets = Ticket.query.filter_by(group_id=current_user.group_id).all()
    return render_template("dashboard.html", tickets=tickets)


@app.route("/ticket/<int:id>", methods=["GET", "POST"])
@login_required
def ticket(id):
    ticket = Ticket.query.get_or_404(id)
    if request.method == "POST":
        if current_user.role.name == "Admin" or (
            current_user.role.name in ["Manager", "Analyst"]
            and current_user.group_id == ticket.group_id
        ):
            ticket.status = request.form["status"]
            ticket.note = request.form["note"]
            db.session.commit()
            flash("Ticket updated successfully.")
        else:
            flash("You do not have permission to update this ticket.")
    return render_template("ticket.html", ticket=ticket)


@app.route("/create_ticket", methods=["GET", "POST"])
@login_required
def create_ticket():
    if request.method == "POST":
        status = request.form["status"]
        note = request.form["note"]
        group_id = (
            current_user.group_id
            if current_user.role.name != "Admin"
            else request.form["group_id"]
        )

        ticket = Ticket(
            status=status, note=note, group_id=group_id, user_id=current_user.id
        )
        db.session.add(ticket)
        db.session.commit()
        flash("Ticket created successfully.")
        return redirect(url_for("dashboard"))
    return render_template("create_ticket.html")
