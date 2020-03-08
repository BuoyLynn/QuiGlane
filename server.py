from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, url_for, flash
from flask_debugtoolbar import DebugToolbarExtension
# from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from model import User, Site, Dive, connect_to_db, db
from forms import Register, Login, Review
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config["SECRET_KEY"] = "quiglane"
app.jinja_env.undefined = StrictUndefined
bcrypt = Bcrypt(app)


@app.route("/")
def home():
    return render_template("home.html", title="Welcome!")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(user_name=form.user_name.data).one()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f"Welcome back {form.user_name.data}!", "success")
            return redirect(url_for("home"))
        else:
            flash("Login fail. Please check your username & password", "danger")
    return render_template('login.html', title="Login", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = Register()
    if form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(user_name=form.user_name.data, email=form.email.data, password=password_hash, twitter=form.twitter.data)
        
        db.session.add(user)
        db.sesion.commit()

        flash(f"Welcome {form.user_name.data}! Registration successful.", "warning")
        return redirect(url_for("home")) # Redirect to the FUNCTION NAME not route

    return render_template("register.html", title="Get Diving!", form=form)


@app.route("/profile/<user_name>")
@login_required
def profile:
    render_template()









if __name__ == "__main__":

    app.debug = True
    
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)
    
    app.run(port=5000, host="0.0.0.0")