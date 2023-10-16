# Built-In Modules

# external Modules
from datetime import datetime

from flask import Blueprint, redirect, render_template, request, session, url_for

from autonomous import log
from autonomous.auth import AutoUser, GithubAuth, GoogleAuth

auth_page = Blueprint("auth", __name__)


@auth_page.route("/login", methods=("GET", "POST"))
def login():
    session["user"] = None
    last_login = datetime(session["user"]["last_login"]) == datetime.now()
    if session.get("user"):
        last_login = datetime.fromisoformat(session["user"]["last_login"])
        diff = datetime.now() - last_login
        if diff.days < 30 and session["user"]["state"] == "authenticated":
            return redirect(url_for("index.index"))
        else:
            session["user"] = None
    if request.method == "POST":
        if request.form.get("authprovider") == "google":
            authorizer = GoogleAuth()
            session["authprovider"] = "google"
        elif request.form.get("authprovider") == "github":
            authorizer = GithubAuth()
            session["authprovider"] = "github"
        uri, state = authorizer.authenticate()
        session["authprovider_state"] = state
        # log(uri, state)
        return redirect(uri)
    else:
        return render_template("login.html")


@auth_page.route("/authorize", methods=("GET", "POST"))
def authorize():
    # log(request.args)
    if session["authprovider"] == "google":
        authorizer = GoogleAuth()
    elif session["authprovider"] == "github":
        authorizer = GithubAuth()
    response = str(request.url)
    # log(response)
    user_info, token = authorizer.handle_response(
        response, state=request.args.get("state")
    )
    user = AutoUser.authenticate(user_info, token)
    session["user"] = user.serialize()
    return redirect(url_for("auth.login"))


@auth_page.route("/logout", methods=("POST",))
def logout():
    if session.get("user"):
        user = AutoUser(pk=session["user"]["pk"])
        user.auth["state"] = "unauthenticated"
        user.save()
        session.pop("user")
        # log(f"User {user.name} logged out")
    return redirect(url_for("auth.login"))
