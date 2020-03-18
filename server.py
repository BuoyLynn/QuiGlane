import os
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_debugtoolbar import DebugToolbarExtension
from forms import Register, Login, Review
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from model import User, Site, Dive, connect_to_db, db

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("appkey")
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
app.jinja_env.undefined = StrictUndefined
bcrypt = Bcrypt(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    marker = Site.query.all()          
    return render_template("home.html", title="Welcome!",
                                        marker=marker)

@app.route("/login", methods=["GET", "POST"])
def login():  
    if current_user.is_authenticated:
        flash(f"Let's get diving { current_user.user_name }!", "success")
        return redirect(url_for("home"))    
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(user_name=form.user_name.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password", "danger")
    
    return render_template('login.html', title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash("See you later gleaner!")
    return redirect(url_for("home"))


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
        return redirect(url_for("login")) # Redirect to the FUNCTION NAME not route

    return render_template("register.html", title="Get Diving!", form=form)


# @app.route("/add-dive/new", methods = ("GET", "POST"))
# # @login_required
# def add_dive():
#     form = Review()
#     if form.validate_on_submit():
#         # if site does not exist in db, add new row to Site and Dive
#         if form.dive_address.data or form.dive_name.data not in Site.query.filter(address, site_name):       
#             site = Site(site_name=form.dive_name.data, address=form.dive_address.data)
#             dive = Dive(                    
#                         dive_day=form.dive_day.data,
#                         dive_date=form.dive_date.data,
#                         dive_time=form.dive_time.data,
#                         rating=form.rating.data,
#                         safety=form.safety.data,
#                         items=form.items.data
#                         user_id=current_user
#                         site_id = site.site_id                                  
#                         )
#         else:
#             site_info = Site.query.filter(address=form.dive_address.data, site_name=form.dive_name.data)
#             dive = Dive(                    
#                         dive_day=form.dive_day.data,
#                         dive_date=form.dive_date.data,
#                         dive_time=form.dive_time.data,
#                         rating=form.rating.data,
#                         safety=form.safety.data,
#                         items=form.items.data
#                         user_id=current_user
#                         site_id = )                                  
#                         )

#     return render_template('profile.html', title='profile')
    

# @app.route("/profile/<int: user_id>")
# @login_required
# def profile():
#     dives = Dive.query.filter_by(current_user.dives).all()
#     return render_template('profile.html', dives=dives)


if __name__ == "__main__":

    app.debug = True    
    app.jinja_env.auto_reload = app.debug
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    
    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host="0.0.0.0")