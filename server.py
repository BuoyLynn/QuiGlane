from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, url_for, flash, request
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
login = LoginManager(app)
login.login_view = "login"
login.init_app(app)


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    #show a list of dive sites (dict) to be mapped.
    return render_template("home.html", title="Welcome!")


@app.route("/login", methods=["GET", "POST"])
def login():
    """ 
    Get: Land Login page.
    POST: If form is valid, redirect user to the logged-homepage.
    """
    
    if current_user.is_authenticated:
        flash(f"Ready to dive {form.user_name.data}?", "success")
        return redirect(url_for("home"))
    
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(user_name=form.user_name.data).first()
        if user is None or not user.check_password_hash(user.password, form.password.data):
            flash('Invalid username or password')
            return redirect(url_for("login"))
        login_user(user, remember=form.remember.data)
        next = request.args.get("next")
        if not next or url_parse(next).netloc != '':
            next = url_for("home")
        return redirect(url_for("home"))
    return render_template('login.html', title="Login", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = Register()
    if form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(user_name=form.user_name.data, email=form.email.data, password=password_hash) 
        # twitter=form.twitter.data
        
        db.session.add(user)
        db.session.commit()

        flash(f"Welcome {form.user_name.data}! Registration successful.", "warning")
        return redirect(url_for("home")) # Redirect to the FUNCTION NAME not route

    return render_template("register.html", title="Get Diving!", form=form)


# @app.route("/add-dive/<int:dive_id>", methods = ("GET", "POST"))
# @login_required
# def add_dive():
#     form = Review()
#     if form.validate_on_submit():
       
#        dive = Review(dive_day=form.dive_day.data, dive_date=form.dive_date.data, dive_time=form.dive_time.data, rating=form.rating.data, safety=form.safety.data, items=form.items.data)

#        db.session.add(dive)
#        db.session.commit
#        flash("Dive added.")
#        return redirect(url_for("home"))
    


# @app.route("/profile/<int: user_name>", methods=("POST"))
# @login_required
# def profile():
#     pass




if __name__ == "__main__":

    app.debug = True
    
    app.jinja_env.auto_reload = app.debug
    
    connect_to_db(app)

    DebugToolbarExtension(app)
    
    app.run(port=5000, host="0.0.0.0")