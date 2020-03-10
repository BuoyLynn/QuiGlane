import datetime
from sqlalchemy import func

from model import Site, Dive, connect_to_db, db
from server import app


"""
TO DO:

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
    connect_to_db(app)
    db.create_all()

    rating_filename = "fregan_dir_clean.txt"
    load_reviews(rating_filename)
   