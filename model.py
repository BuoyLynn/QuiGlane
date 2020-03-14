from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, time


db = SQLAlchemy()


class User(db.Model):
# class User(db.Model):
    """User of QuiGlane"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_name = db.Column(db.String(35), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    # find a way for users to confirm email address
    password = db.Column(db.String(64), nullable=False)
    # twitter = db.Column(db.String(15), nullable=True)
    dive = db.relationship("Dive", backref='user', lazy=True)
         
    
    def __repr__(self):

        return f"<User user_id={self.user_id} user_name={self.user_name}>"


class Site(db.Model):
    """Diving Site Information"""

    __tablename__ = "sites"

    site_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # business name (ex. Whole Foods)
    site_name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(150), nullable=True)
    # google place_id from site_name & address request
    place_id = db.Column(db.String(150), nullable=True)
    # google request place_id and populate lat & long
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    # type of business (ex. grocery, bakery, etc.)
    category = db.Column(db.String(100), nullable=True)
    open_time = db.Column(db.Time, nullable=True)
    close_time = db.Column(db.Time, nullable=True)
    dive = db.relationship("Dive", backref='site', lazy=True)

    def __repr__(self):

        return f"""<{self.site_id}: {self.site_name} 
                    Lat={self.latitude} Lng={self.latitude}
                    Cat={self.category[0:2]}>"""

class Dive(db.Model):
    """Dive Ratings and Review"""

    __tablename__ = "dives"

    dive_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dive_day = db.Column(db.Integer, nullable=True)
    dive_date = db.Column(db.Date, nullable=True)
    dive_time = db.Column(db.Time, nullable=True, default=datetime.utcnow)
    rating = db.Column(db.Integer, nullable=True)
    safety = db.Column(db.Boolean, nullable=True, default=None)
    items = db.Column(db.String(250), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    site_id = db.Column(db.Integer, db.ForeignKey("sites.site_id"), nullable=False)

    def __repr__(self):

        return f"<Dive @ site_id:{self.site_id} rated {self.rating} by user ID: {self.user_id}>"



#################################
# Connect db to app (server.py)

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///glean'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    # login.init_app(app)


if __name__ == "__main__":
    
    from server import app, login
    connect_to_db(app)
    print("Connected to DB.") # To test in interactive mode


