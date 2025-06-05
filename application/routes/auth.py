"""/application/routes/auth.py"""

from flask import Blueprint, render_template, redirect, make_response, flash, url_for
from flask_jwt_extended import create_access_token, set_access_cookies

from application.forms import LoginForm
from application.models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()

    print(f"[auth.py]: login route initated.")

    if form.validate_on_submit():
        print(f"[auth.py]: form validated")

        username = form.username.data
        password_str = form.password.data


        print(f"[auth.py]: username: {username}, password: {password_str}")

        user = User.query.filter_by(username=username).first()

        print(f"[auth.py]: user: {user}")

        if not user or not user.check_password(password_str):
            flash("Username or password Wrong. Please try again.", "danger")
            return redirect(url_for("auth.login"))
        
        access_token = create_access_token(identity=str(user.id))

        response = make_response(redirect(url_for("main.home")))
        set_access_cookies(response, access_token)

        return response
    else:
        print("[auth.py]: form validation failed")
        print(form.errors)  # << Add this

    return render_template("login.html", form=form)
