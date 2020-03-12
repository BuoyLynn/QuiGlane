import os
import json
import datetime
import requests
from sqlalchemy import func
# import nltk
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def load_db(dirty_directory):
    """populate sites with name and pseudo address (not lat/long), give it a site_id"""

    with open(dirty_directory) as data:
        for row in data:
            site_name, address, parse_detail = row.rstrip().split('.', 2)
            site = Site(site_name = site_name,
                        address = address + ' NY')
            # load parse_detail to dive
            db.session.add(site)        
        db.session.commit()


def add_site_place_id():
    """Query table 'sites' as GOOG Places API requests param input"""
    
    # Loop through row (obj) in db.Site
    for site in Site.query.all():
        # feed API param input string dynamically:
        params = {
                  'key': os.getenv("GOOGKEY"),
                  'input': site.site_name + site.address,
                  'inputtype': 'textquery',
                }
        # Run GOOG PLACES API requests (returns places_id only.)        
        GOOG_PLACES_API = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
        r = requests.get(GOOG_PLACES_API, params = params)
        place_api_returns = r.json()
        # Weed out failed search.
        if place_api_returns['status'] == 'OK':
            place_id = place_api_returns['candidates'][0]['place_id']
        site.place_id = place_id
        db.session.commit()





"""
TO DO:
March 11
Load db table dives with the parse_detail with corresponding site and user_id (freegan)

March 8
open(freegan_dir_clean.txt)
loop through
each line represents a business:
    split on the first two '.': create a list of three strings per line.
    list[0] will be businessname 
    list[1] will be address
        This pseudo address will be cross referenced with google maps to provide lat and long to db.
    list[2] will be processed through nltk.
        1. tokenize words. (from nltk.tokenzie import word_tokenize)
        2. remove punctuation. (from nltk.corpus import stopwords)
        3. remove stopwords.
        4. run Parts of Speech (POS) on tokens.
            ** Do more research on NLP POS Tags, aka study grammar for better information extraction (documentation: https://www.nltk.org/book/ch07.html) to parse and place in respective db table & columns.
            THEN: nltk.pos_tag() to generate (token, POS tag) tuples.
            AND, run Named Entity Recognition (USE SpaCy: https://spacy.io/api/annotation#section-named-entities) ** read SpaCy API

All entries will be associated with user (foreignkey) #1 freegan.org. precreated before session.add() and session.commit

"""


if __name__ == "__main__":
    from server import app
    from model import User, Site, Dive, connect_to_db, db

    connect_to_db(app)
    db.create_all()
    
    dirty_directory = "seed_data/freegan_dir_clean.txt"
    # load_db(dirty_directory)