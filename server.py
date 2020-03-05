from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, url_for, flash
# from flask_debugtoolbar import DebugToolbarExtension
from model import User, Site, Dive, connect_to_db, db
from forms import Register, Login


app = Flask(__name__)

app.config["SECRET_KEY"] = "quiglane"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def home():
    return render_template("home.html", title="Welcome!")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = Register()
    if form.validate_on_submit():
        flash(f"Welcome {form.user_name.data}! Registration successful.", "warning")
        return redirect(url_for("home")) # Redirect to the FUNCTION NAME not route

    return render_template("register.html", title="Get Diving!", form=form)

@app.route("/login")
def login():
    form = Login()
    return render_template("login.html", title="Dive in!", form=form)








if __name__ == "__main__":

    app.debug = True
    
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(port=5000, host="0.0.0.0")