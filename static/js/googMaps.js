
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
          position: uluru,
          map: map,
          title: 'Silver Moon'
        });
        marker.addListener('click', function() {
          infowindow.open(map, marker);
        });
      }
