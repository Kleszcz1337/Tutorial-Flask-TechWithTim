from flask import Blueprint, render_template

second = Blueprint("second", __name__, static_folder="static", template_folder="templates")

#http://127.0.0.1:5000/admin
@second.route("/home")
@second.route("/")
def home():
    return render_template("home.html")

#http://127.0.0.1:5000/admin/test
@second.route("/test")
def test():
    return "<h1>test second.py</h1>"