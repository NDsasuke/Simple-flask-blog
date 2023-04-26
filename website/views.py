from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
@login_required
def home():
    return render_template("home.html", name=current_user.username)

@views.route('/create', methods=('GET', 'POST'))
def create():
      return render_template('create.html')

@views.route('/terms', methods=('GET', 'POST'))
def terms():
      return render_template('terms.html')