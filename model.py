from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


#################################
# Model Definitions

class User(db.Model):
    """User of QuiGlane"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_name = db.Column(db.String(35), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False)
    # find a way for users to confirm email address
    password = db.Column(db.String(64), nullable=False)
    # figure out a way to hash passwords
    twitter = db.Column(db.String(15), nullable=True)
         
    
    def __repr__(self):

        return f"<User user_id={self.user_id} user_name={self.user_name}>"


class Site(db.Model):
    """Diving Site Information"""

    __tablename__ = "sites"

    site_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # business name (ex. Whole Foods)
    site_name = db.Column(db.String(150), nullable=False)
    # type of business (ex. grocery, bakery, etc.)
    category = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(150), nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    # put in column geo to use GeoAlchemy
    open_time = db.Column(db.DateTime, nullable=True)
    close_time = db.Column(db.DateTime, nullable=True)

    def __repr__(self):

        return f"<Site={self.site_name} ID={self.site_id}>"

class Dive(db.Model):
    """Dive Ratings and Review"""

    __tablename__ = "dives"

    dive_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dive_day = db.Column(db.Integer, nullable=False)
    dive_date = db.Column(db.Date, nullable=False)
    dive_time = db.Column(db.Time, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    safety = db.Column(db.Boolean, nullable=False, default=None)
    items = db.Column(db.String(250), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    site_id = db.Column(db.Integer, db.ForeignKey("sites.site_id"), nullable=False)

    user = db.relationship("User", backref="dives")
    site = db.relationship("Site", backref="sites")

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


if __name__ == "__main__":
    
    from server import app
    connect_to_db(app)
    print("Connected to DB.") # To test in interactive mode
