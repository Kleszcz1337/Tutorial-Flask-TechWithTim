from flask import Flask, render_template
from admin.second import second

app = Flask(__name__)
app.register_blueprint(second, url_prefix="/admin")
# blueprinty zloża nam do przekazywania pewnych dzialnian do innego plik .py 
# np. dla /admin chcemy robić zupelnie inne rzeczy niz dla usera zwyczjanego
# np. po /admin bedziemy wysweitlac inny wyglad strony
# blue print wlaczy sie tylko wteyd kiedyu bedzie prefix /admin

@app.route("/")
def home():
    return "<h1>TEST main.py</h1>"

if __name__ == "__main__":
    app.run(debug=True)