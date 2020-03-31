import os
import json
import requests
from model import SQLAlchemy, datetime, Site, Dive, User, time, connect_to_db, db


db = SQLAlchemy()

# In server, will be passing params (form.dive_name.data, form.dive_name.data)
def run_goog_places_api(site_name, address, created_site):
    """ Add to site details """
    
    # Query site by newly created site_id
    update_site = created_site
    
    # Set parameters for GOOGLE place_id search
    params = {
              'key': os.getenv("GOOGKEY"),
              'input': site_name + " " + address,
              'inputtype': 'textquery',
             } 
    
    # Run GOOG PLACES API requests (returns places_id only.)        
    GOOG_PLACES_API = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
    r = requests.get(GOOG_PLACES_API, params = params)
    
    # Jasonify request returns
    place_api_returns = r.json()
    
    # Check if Google places_id has found:   
    if place_api_returns['status'] == 'OK':
        place_id = place_api_returns['candidates'][0]['place_id']

        update_site.place_id = place_id
        
        # With place_id set as parameter get additinal info from GOOG Places API and populate
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
            
            update_site.latitude = lat
            update_site.longitude = lng

            # check if category exits, if so, get upto 4 categories listed.
            if 'types' in site_details['result']:
                category_list = site_details['result']['types'][0:4]
                category_string = ', '.join(category_list)
                category = category_string     

                update_site.category = category       
            
            # check if opening_hours exist in json
            if 'opening_hours' in site_details['result']:                
                open_t = site_details['result']['opening_hours']['periods'][0]['open']['time']

                update_site.open_time = time(hour=int(open_t[0:2]), minute=int(open_t[2:4]))
                
                # check if closing hour exists:
                # if no close time, 24h open business. Set close time to "0000"
                if 'close' in site_details['result']['opening_hours']['periods'][0]:
                    close_t = site_details['result']['opening_hours']['periods'][0]['close']['time']                   
                else:
                    close_t = open_t

                update_site.close_time = time(hour=int(close_t[0:2]), minute=int(close_t[2:4]))

               

if __name__ == "__main__":
    
    from server import app, login_manager
    
    connect_to_db(app)
    print("Connected to DB.") # To test in interactive mode





    
    



  