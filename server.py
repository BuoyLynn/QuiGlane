# import os
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, url_for, flash, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension
from forms import Register, Login, Review
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from model import User, Site, Dive, connect_to_db, db, datetime
from helpload import run_goog_places_api, os

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("appkey")
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
app.jinja_env.undefined = StrictUndefined
bcrypt = Bcrypt(app)

@login_manager.user_loader
def load_user(user_id):
    """User login manager -> will check for current_user"""
    return User.query.get(int(user_id))

@app.route("/")
def home():
    """Route to App home"""
    marker = Site.query.all()          
    return render_template("home.html", title="Go Glean!",
                                        marker=marker)


@app.route('/api/sites-info')
def site_info():
    """JSON to seed markers on Google Maps API"""
    sites_dives = db.session.query(Site, Dive).outerjoin(Dive).all()    
    make_info_json = []
    for site, dive in sites_dives:
        # convert all time to string to jasonify
        if dive.dive_time: # otherwise will through error, nonetype cannot be strftime
            dive.dive_time = dive.dive_time.strftime('%H%M')            
        else:
            dive.dive_time = 'Not Specified'
            
        if site.open_time or site.close_time:
        # if time is a str, convert to datettime
            if type(site.open_time) == str:
                open_time = datetime(site.open_time)
                open_time = open_time.strftime('%H%M')
                close_time = datetime(site.close_time)
                close_time = close_time.strftime('%H%M')
            # else run strftime            
            open_time = site.open_time.strftime('%H%M')
            close_time = site.close_time.strftime('%H%M')
        
            
            site_info = {'lat': site.latitude, 
                        'lng': site.longitude,
                        'business': site.site_name,
                        'address': site.address,
                        'category': site.category,
                        'open': open_time,
                        'close': close_time,
                        'dive_day': dive.dive_day,
                        'dive_time': dive.dive_time,
                        'rating': dive.rating,
                        'safety': dive.safety,
                        'details': dive.items                
                        }
            make_info_json.append(site_info)
    
    return jsonify(make_info_json)


@app.route('/api/sites-autocomp')
def site_autocomp():
    """JSON to feed autocomplete in new-dive forms"""
    sites = db.session.query(Site.site_name, Site.address).all()
    site_name_auto_json = []
    for site in sites:
        site = {'site_name': site[0],
                'address': site[1]}
        site_name_auto_json.append(site)
    
    return jsonify(site_name_auto_json)
                

@app.route("/login", methods=["GET", "POST"])
def login():
    """Login verification"""  
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
    flash("See you later gleaner!", "warning")
    return redirect(url_for("home"))


@app.route("/register", methods=["GET", "POST"])
def register():
    """User verification using forms: Will fail or validate on submit"""
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


@app.route("/add-dive/new", methods = ("GET", "POST"))
@login_required
def add_dive():
    """Add new dive reivew
        1. If site exists, take existing(matching) site_id and add to dive table.
        2. If site does not exist, add new site, populate site information with the helpload (runs GOOG Places API) then add new dive review.
    """
    form = Review()
    if request.method == "POST":
    # if form.validate_on_submit():
       
        dive_address = form.dive_address.data
        dive_name = form.dive_name.data
        # Query Site from db .
        site = Site.query.filter(Site.site_name==dive_name, Site.address==dive_address).first()
        # If a match
        if site != None:
                          
            dive = Dive(                    
                        dive_day=form.dive_day.data,
                        dive_date=form.dive_date.data,
                        dive_time=form.dive_time.data,
                        rating=form.rating.data,
                        safety=form.safety.data,
                        items=form.items.data,
                        user_id=current_user.user_id,
                        site_id = site.site_id
                        )

            db.session.add(dive)
            db.session.commit()
           
        # if site not in db, add new row to 'sites' run goog api and populate Dive
        else:

            create_site = Site(site_name=dive_name, address=dive_address)
            db.session.add(create_site)
            db.session.commit()

            created_site = Site.query.filter(Site.site_name==dive_name, Site.address==dive_address).first()

            # run goog places api on new site to populate remaining fields
            run_goog_places_api(dive_name, dive_address, created_site.site_id)
            
            # add remaining dive review to db
            dive = Dive(                    
                        dive_day=form.dive_day.data,
                        dive_date=form.dive_date.data,
                        dive_time=form.dive_time.data,
                        rating=form.rating.data,
                        safety=form.safety.data,
                        items=form.items.data,
                        user_id=current_user.user_id,
                        site_id = created_site.site_id
                        )
            
            db.session.add(dive)
            db.session.commit()    

        # flash in dive_cards if successful
        flash(f"Thanks, {current_user.user_name}! Your dive has been added to your profile. You can now look up similar dives.", "success")
        return redirect(url_for("dive_cards", user_id=current_user.user_id))    
   
    return render_template("newdive.html", title="Save the Dive!", form=form)
    

@app.route("/dive-cards/<int:user_id>")
@login_required
def dive_cards(user_id):
    """User's profile page loads all dive reviews as cards (see template)"""
    user = User.query.filter_by(user_id=user_id).first_or_404()
    dives = Dive.query.filter_by(user_id=user_id).all()
    return render_template('profile.html', title=user.user_name, dives=dives)


@app.route("/dive-cards/<int:dive_id>/update", methods=["GET", "POST"])
@login_required
def update_dive(dive_id):
    """Update dive review while verifying current_user as author"""
    update_dive = Dive.query.get(dive_id)
    site = Site.query.filter_by(site_id=update_dive.site_id).first()
    if update_dive.user_id != current_user.user_id:
        
        flash("Hey! Who dares to pilfer another's glean?", "danger")
        return redirect(url_for("home"))
    
    form = Review()
    if request.method == "POST":
        update_dive.dive_day = form.dive_day.data
        update_dive.dive_date = form.dive_date.data
        update_dive.dive_time = form.dive_time.data
        update_dive.rating = form.rating.data
        update_dive.safety = form.safety.data
        update_dive.items = form.items.data
        
        db.session.commit()

        flash(f"Your dive was successfully updated.", "success")
        return redirect(url_for("dive_cards", user_id=current_user.user_id))
    
    # Open update forms pre-populated with data
    elif request.method == "GET":
        form.dive_day.data = update_dive.dive_day
        form.dive_date.data = update_dive.dive_date
        form.dive_time.data = update_dive.dive_time
        form.rating.data = update_dive.rating
        form.safety.data = update_dive.safety
        form.items.data = update_dive.items
    
    return render_template("updatedive.html", title="Dive Update", form=form, update_dive=update_dive, site=site)


@app.route("/dive-cards/<int:dive_id>/delete", methods=["POST"])
@login_required
def delete_dive(dive_id):
    """Delete dive while verifying that current_user is author of dive"""
    delete_dive = Dive.query.get(dive_id)
    if delete_dive.user_id != current_user.user_id:
        
        flash("Careful this is not your glean to delete! Karma karma karma.", "danger")
        return redirect(url_for("home"))
    
    db.session.delete(delete_dive)
    db.session.commit()

    flash(f"Your dive review was deleted. Hope to see you add another soon!", "dark")
    return redirect(url_for("dive_cards", delte_dive=delete_dive, user_id=current_user.user_id))


@app.route("/site-cards/<int:site_id>")
@login_required
def get_site_cards(site_id):
    """Via user's dive, allow access to other dive reivews matching the site"""
    site = Site.query.filter_by(site_id=site_id).first_or_404()
    site_dives = Dive.query.filter_by(site_id=site_id).all() 
    return render_template('dives-from-card.html', title=site.site_name, site_dives=site_dives, site=site)


if __name__ == "__main__":

    app.debug = True    
    app.jinja_env.auto_reload = app.debug
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    
    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host="0.0.0.0")