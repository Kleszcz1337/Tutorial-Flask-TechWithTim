from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return "Home page"

@app.route("/<name>")
def user(name):
    return f"Hello {name} !"

@app.route("/admin")        #podajmy nazwe funkcji w "" zeby przekierowac
def admin():                #jezeli funkcja ma paramentry to podajemy je po , z nazwa
    return redirect(url_for("user" , name="Admin!"))

@app.route("/template/<name>")
def template(name):         #za pomoca zmiennej content posylamy do fronendu dane
    return render_template("index.html", content=name, r="r22r")

@app.route("/content")
def contentt():
    return render_template("index2.html", content=["tim", "joe", "bill"])

if __name__ == "__main__":
    app.run() 