"""/application/routes/auth.py"""

from flask import Blueprint, render_template, request, redirect, make_response, flash, url_for
from flask_jwt_extended import jwt_required, create_access_token, set_access_cookies, unset_jwt_cookies

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

        # print(f"[auth.py]: username: {username}")

        try:
            user = User.query.filter_by(username=username).first()

            if not user or not user.check_password(password_str):
                flash("Username or password wrong. Please try again.", "danger")
                return redirect(url_for("auth.login"))

            access_token = create_access_token(identity=str(user.id))

            response = make_response(redirect(url_for("main.home")))
            set_access_cookies(response, access_token)
            return response

        except Exception as e:
            print(f"[auth.py] ⚠️ Exception during login: {e}")
            flash("Something went wrong during login. Please try again later.", "danger")
            return redirect(url_for("auth.login"))
    else:
        print("[auth.py]: form validation failed")
        print(form.errors)  # << Add this

    return render_template("login.html", form=form)


@auth_bp.route("/logout", methods=["GET"])
@jwt_required()
def logout():
    print(f"[auth.py] request: {request}")
    response = make_response(redirect(url_for("auth.login")))
    print(f"[auth.py] response: {response}")
    unset_jwt_cookies(response)
    
    return response



