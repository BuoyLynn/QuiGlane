import os
import json
import datetime
import requests
from sqlalchemy import func
# import nltk
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, time


db = SQLAlchemy()


def load_site_freegan():
    """populate sites with name and pseudo address (not lat/long), give it a site_id"""

    with open(dirty_directory) as data:
        for row in data:
            site_name, address, parse_detail = row.rstrip().split('.', 2)
            site = Site(site_name = site_name.strip(),
                        address = address.strip() + ' NY')
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
                  'input': site.site_name + " " + site.address,
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
    

def add_site_details():
    """Request GOOGLE PLACES API using site.places_id (from add_site_place_id())"""
    
    # Loop site(obj) db.Site
    for site in Site.query.all():
        # feed API param place_id dynamically:
        params = {
                  'key': os.getenv("GOOGKEY"),
                  'place_id': site.place_id,
                 }
        # Run GOOG PLACES API requests for place details      
        GOOG_PLACES_API = 'https://maps.googleapis.com/maps/api/place/details/json'
        r = requests.get(GOOG_PLACES_API, params = params)
        site_details = r.json()
        # Create json file for future use. (didn't work...)
        with open('site_details.json', 'w') as site_details_json:
            json.dump(site_details, site_details_json)
        # Weed out failed search. and grab details
        if site_details['status'] == 'OK':
            lat = site_details['result']['geometry']['location']['lat']
            lng = site_details['result']['geometry']['location']['lng']            
            # check if category exits, if so, get category.
            if 'types' in site_details['result']:
                category_list = site_details['result']['types'][0:4]
                category_string = ', '.join(category_list)
                category = category_string            
            # check if opening_hours exist in json
            if 'opening_hours' in site_details['result']:                
                open_t = site_details['result']['opening_hours']['periods'][0]['open']['time']
                # check if closing hour exists:
                # if no close time, 24h open business. Set close time to "0000"
                if 'close' in site_details['result']['opening_hours']['periods'][0]:
                    close_t = site_details['result']['opening_hours']['periods'][0]['close']['time']                   
                else:
                    close_t = open_t            
        # add to db.Site columns open_time & close_time
                site.latitude = lat
                site.longitude = lng
                site.category = category
                site.open_time = time(hour=int(open_t[0:2]), minute=int(open_t[2:4]))
                site.close_time = time(hour=int(close_t[0:2]), minute=int(close_t[2:4]))
        # commit to database
        db.session.commit()


def add_dive():
    """cross reference with """
    # 1.open dirty_directory   
    with open(dirty_directory) as data:
        for row in data:
            data_name, data_address, details = row.rstrip().split('.', 2)
            data_name = data_name.strip()
            data_address = data_address.strip() + ' NY' # To match db sites.address
            # 2. check site_name from dirty_diretory and add site_id to dives
            # and user id is freegam (2)            
            dive = Dive(items = details.strip(),
                        site_id = db.session.query(Site.site_id).filter(Site.site_name==data_name, Site.address==data_address).first()[0],
                        user_id = db.session.query(User.user_id).filter(User.user_name=='freegan').first()[0])
        
            db.session.add(dive)        
        db.session.commit()
            
            


if __name__ == "__main__":
    from server import app
    from model import User, Site, Dive, connect_to_db, db

    connect_to_db(app)
    db.create_all()
    
    dirty_directory = "seed_data/freegan_dir_clean.txt"
  