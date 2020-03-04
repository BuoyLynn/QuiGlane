from jinja2 import StrictUndefined
from flask import Flask
# from flask_debugtoolbar import DebugToolbarExtension
from model import User, Site, Dive, connect_to_db, db


app = Flask(__name__)

app.secret_key = "quiglane"

app.jinja_env.undefined = StrictUndefined

if __name__ == "__main__":

    app.debug = True
    
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')