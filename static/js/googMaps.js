// function initMap() {
//     // Replace hard code into dynamic input from db.
//     var silverMoonBakery = {lat: 40.800518, lng: -73.967671};
//     // The map, centered silverMoonBakery - make this dynamic to current location if not default ny,ny
//     var map = new google.maps.Map(
//         document.getElementById('map'), {zoom: 15, center: silverMoonBakery});
//     // The marker, silverMoonBakery
//     var marker = new google.maps.Marker({position: silverMoonBakery, map: map});
//   }

// This example displays a marker at the center of Australia.
// When the user clicks the marker, an info window opens.

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


      ////////////////
 // This example displays a marker at the center of Australia.
      // When the user clicks the marker, an info window opens.

// function initMap() {
// var uluru = {lat: -25.363, lng: 131.044};
// var map = new google.maps.Map(document.getElementById('map'), {
//     zoom: 4,
//     center: uluru
// });

// var contentString = '<div id="content">'+
//     '<div id="siteNotice">'+
//     '</div>'+
//     '<h1 id="firstHeading" class="firstHeading">Uluru</h1>'+
//     '<div id="bodyContent">'+
//     '<p><b>Uluru</b>, also referred to as <b>Ayers Rock</b>, is a large ' +
//     'sandstone rock formation in the southern part of the '+
//     'Northern Territory, central Australia. It lies 335&#160;km (208&#160;mi) '+
//     'south west of the nearest large town, Alice Springs; 450&#160;km '+
//     '(280&#160;mi) by road. Kata Tjuta and Uluru are the two major '+
//     'features of the Uluru - Kata Tjuta National Park. Uluru is '+
//     'sacred to the Pitjantjatjara and Yankunytjatjara, the '+
//     'Aboriginal people of the area. It has many springs, waterholes, '+
//     'rock caves and ancient paintings. Uluru is listed as a World '+
//     'Heritage Site.</p>'+
//     '<p>Attribution: Uluru, <a href="https://en.wikipedia.org/w/index.php?title=Uluru&oldid=297882194">'+
//     'https://en.wikipedia.org/w/index.php?title=Uluru</a> '+
//     '(last visited June 22, 2009).</p>'+
//     '</div>'+
//     '</div>';

// var infowindow = new google.maps.InfoWindow({
//     content: contentString
// });

// var marker = new google.maps.Marker({
//     position: uluru,
//     map: map,
//     title: 'Uluru (Ayers Rock)'
// });
// marker.addListener('click', function() {
//     infowindow.open(map, marker);
// });
// }