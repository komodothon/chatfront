"""/app/routes/auth.py"""

from flask import Blueprint, render_template, redirect, make_response, flash, url_for
from flask_jwt_extended import create_access_token, set_access_cookies

from app.forms import LoginForm
from app.models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password_str = form.password.data

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password_str):
            flash("Username or password Wrong. Please try again.", "danger")
            return redirect(url_for("auth.login"))
        
        access_token = create_access_token(identity=str(user.id))

        response = make_response(redirect(url_for("main.home")))
        set_access_cookies(response, access_token)

        return response

    return render_template("login.html", form=form)
