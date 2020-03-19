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




function initMap() {
var silverMoonBakery = {lat: 40.800518, lng: -73.967671};
var map = new google.maps.Map(document.getElementById('map'), 
                                {zoom: 15, center: silverMoonBakery});
// Replace content string with Data.details that matches the site_id of lat/long in loop
var contentString = '<div id="content">'+
    '<div id="siteNotice">'+
    '</div>'+
    '<h1 id="firstHeading" class="firstHeading">Silver Moon Bakery</h1>'+
    '<div id="bodyContent">'+
    '<p>We found meat and cheese sandwiches as well as bread.</p>'+
    '<p>Category: [from Site.category]</p>'+
    '<p>(last visited [time stamp from Data.date, time]).</p>'+
    '</div>'+
    '</div>';

var infowindow = new google.maps.InfoWindow({
    content: contentString
});

var marker = new google.maps.Marker({
    position: silverMoonBakery,
    map: map,
    title: 'Silver Moon'
});
marker.addListener('click', function() {
    infowindow.open(map, marker);
});
}
