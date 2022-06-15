from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5) #ustawimy ile ma trwac sesja uzytkownika

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

    

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all())


@app.route("/login", methods=["POST", "GET"])
def login():
    if(request.method == "POST"):
        session.permament = True
        #w tym miejscu pobieramy wartość z dokladnego pola poprzez "nm"
        #taka sama wartosc jak w html zmienna name="nm"
        user = request.form["nm"] #using key to get exl. this form
        session["user"] = user #tak ustawiamy sesja dla uzytwkonika
        
        #mozesz np wyszukac name="michal"
        #.first daje ci pierwszego michala
        #zeby dostawc wszystkich uzyj .all(), usuwasz .delete()
        found_user = users.query.filter_by(name=user).first() #znajdowanie konkretnego uzytkownika

        if found_user: #sprawdz czy uzytwkonik istnieje juz
            session["email"] = found_user.email #grabbing data from database to session
        else:
            usr = users(user, " ")
            db.session.add(usr)
            db.session.commit()
        
        flash(f"Zalogowales sie poprawnie {user}", "info")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            user = session["user"]
            flash(f"Juz jestes zalogowany {user}", "info")
            return redirect(url_for("user"))
        else:
            return render_template("login.html")

@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:           #jezeli uztwkonik jest w sesji
        user = session["user"]      #to pobieramy go za pomoca klucza "user"

        if request.method == "POST": #jezeli dostalismy postem maila to zapisujemy go do sesji
            email = request.form["email"] #pobiera nam z htmlowskiego forma email
            session["email"] = email

            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()

            flash("Email saved")
        else:
            if "email" in session:
                email = session["email"]

        return render_template("user.html",email=email)
    else:
        flash("Nie jestes zalogowany", "info")
        return redirect(url_for("login"))       #podajemy nazwe funkcji, nie strony!

@app.route("/logout")
def logout():
    if "user" in session:
         user = session["user"]
         flash(f"Wylogowales sie poprawienie {user}", "info")
    #None dlatego żeby usunąć dana sesje z session, zastapic ja po prostu None
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)