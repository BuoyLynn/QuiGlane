/* 
var [LOCATION/MARKER]
lat = Site.latitude
lng = Site.longitude

var [map]
center: current_user's current location (GEOLOCATION)

var [contentString]
<h1>{{ Site.address }}</h1>
<p><small><b>Category:</b>{{ Site.category }}</small></p>
<p>{{ Dive.items }}
<p>...etc etcn Dive.dive_time, Dive.safety

var [marker]
if current_time in time_delta=Site.open and Site.close:
    then show markers within given radius (refer to zoom).
Else:
    hide marker.
*/


function initMap(){

    // draw base map centering to NY
    var map = new google.maps.Map(document.getElementById("map"),{
        center: new google.maps.LatLng(40.7829, -73.9654),
        zoom: 15
    }); // close base map

    const jsonUrl = "/api/sites-info";    
    $.get(jsonUrl, (siteData) => {
       
        for (let site of siteData) {
           
            if (site.lat !== null){
            let latlng = {"lat": site.lat, "lng": site.lng}; 
            let siteTitle = site.business;

            // Plot markers on the map using json data
            const marker = new google.maps.Marker({ position: latlng,
                                                    map: map,
                                                    title: siteTitle
                                                    }); // close marker
            if (site.close !== 0){
            let closeTime = site.close.slice(0, 2) +":"+ site.close.slice(2, 5);     
            let diveTime = site.dive_time.slice(0, 2) +':'+ site.dive_time.slice(2, 5);
            
            // Pop up box content
            const contentString = '<div id="content">'+
            '<div id="siteNotice">'+
            '</div>'+
            '<h1 id="firstHeading" class="firstHeading">'+ siteTitle +'</h1>'+
            '<p><small>Category: ' + site.category + '</small></p>'+
            '<div id="bodyContent">'+
            '<p>' + site.details +'</p>'+            
            '<p>Business closes at '+ closeTime +'</p>'+
            '<p>Last dive time reported at '+ diveTime +'</p>'+
            '<p>Most recent dive rated: ' + site.rating + '</p>'+
            '<p>with Safety details: ' + site.safety + '</p>'+
            '</div>'+
            '</div>';
            // Create popup box
            const infowindow = new google.maps.InfoWindow({
                content: contentString
            });                   
            // event listener for marker, popup at click
            marker.addListener('click', function() {
                infowindow.open(map, marker);               
            }); //close marker
        } // close time if
        }//close lat if
        }; // close forloop
    }); // close ajax get request (call back function)
    } // close initMap

