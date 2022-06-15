from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "secret_key"
app.permanent_session_lifetime = timedelta(minutes=5) #ustawimy ile ma trwac sesja uzytkownika

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if(request.method == "POST"):
        session.permament = True
        #w tym miejscu pobieramy wartość z dokladnego pola poprzez "nm"
        #taka sama wartosc jak w html zmienna name="nm"
        user = request.form["nm"] #using key to get exl. this form
        session["user"] = user #tak ustawiamy sesja dla uzytwkonika
        flash(f"Zalogowales sie poprawnie {user}", "info")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            user = session["user"]
            flash(f"Juz jestes zalogowany {user}", "info")
            return redirect(url_for("user"))
        else:
            return render_template("login.html")

@app.route("/user")
def user():
    if "user" in session: #jezeli uztwkonik jest w sesji
        user = session["user"]#to pobieramy go za pomoca klucza "user"
        return render_template("user.html", user=user)
    else:
        flash("Nie jestes zalogowany", "info")
        return redirect(url_for("login"))#podajemy nazwe funkcji, nie strony!

@app.route("/logout")
def logout():
    if "user" in session:
         user = session["user"]
         flash(f"Wylogowales sie poprawienie {user}", "info")
    #None dlatego żeby usunąć dana sesje z session, zastapic ja po prostu None
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)