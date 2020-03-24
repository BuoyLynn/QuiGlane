import os
import json
import requests
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, time

db = SQLAlchemy()

# In server, will be passing params (form.dive_name.data, form.dive_name.data)
def run_goog_places_api(site_name, address, site_id):
    
    # update_site = site.query.filter_by(site_id=site_id).first()

    params = {
              'key': os.getenv("GOOGKEY"),
              'input': site_name + " " + address,
              'inputtype': 'textquery',
             } 
    # Run GOOG PLACES API requests (returns places_id only.)        
    GOOG_PLACES_API = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
    r = requests.get(GOOG_PLACES_API, params = params)
    place_api_returns = r.json()
       
    if place_api_returns['status'] == 'OK':
        place_id = place_api_returns['candidates'][0]['place_id']
        
        # As place_id returns, get other info from GOOG Places and populate
        params = {
                  'key': os.getenv("GOOGKEY"),
                  'place_id': place_id,
                 }

        # Run GOOG PLACES API requests for place details      
        GOOG_PLACES_API = 'https://maps.googleapis.com/maps/api/place/details/json'
        r = requests.get(GOOG_PLACES_API, params = params)
        site_details = r.json()
        
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
                new_site = Site(site_name=dive_name, 
                                address=dive_address,
                                place_id=place_id,
                                latitude=lat,
                                longitude=lng,
                                category=category,
                                open_time=time(hour=int(open_t[0:2]), minute=int(open_t[2:4])),
                                close_time=time(hour=int(close_t[0:2]), minute=int(close_t[2:4]))
                                )
                db.session.add(new_site)
                db.session.commit()
        



    
    



  