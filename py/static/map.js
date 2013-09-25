google.maps.event.addDomListener(window, 'load', initialize_map);

function initialize_map() {
    var myLatlng = new google.maps.LatLng(42.28, 83.75);
    var mapOptions = {
        center: myLatlng, 
        zoom: 6,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById("map-canvas"),
                                  mapOptions);
    var city_marker = new google.maps.Marker({
            position: myLatlng,
            map: map,
	});
}

function switch_map(cities) {
    var mainCityLatLng = new google.maps.LatLng(cities[0]['lat'], cities[0]['lng']);
 
    var mapOptions = {
	center : mainCityLatLng, 
	zoom: 6, 
	mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById("map-canvas"),
				  mapOptions); 
    var image = {
	url: 'city_icon.png', 
	size: new google.maps.Size(20,30), 
	origin: new google.maps.Point(0,0), 
	anchor: new google.maps.Point(0,30), 
    };
    var markers = []; 
    var bounds = new google.maps.LatLngBounds();
    for(var i = 0; i < cities.length; i++){
	createMarker(cities[i]['lat'], cities[i]['lng'], markers, map);
	bounds.extend(new google.maps.LatLng(cities[i]['lat'], cities[i]['lng']));
    }
    plotTravelPath(cities, map);
    map.fitBounds(bounds);
}

function createMarker(lat, lng, markers, map){
    markers.push(new google.maps.Marker({
	    position: new google.maps.LatLng(lat, lng),
	    map: map 
		    })); 
}

function testSwitch(){
    switch_map([
		{lat:'51.5', lng:'.13'}, 
		{lat:'53', lng: '.52'}, 
		{lat:'54', lng: '1.1'}, 
		{lat:'52', lng: '2.15'}
		]);
}

function plotTravelPath(cities, map){
    var city_coords = [];
    for(var i = 0; i < cities.length; i++){
	var city = cities[i]; 
	city_coords.push(new google.maps.LatLng(city['lat'], city['lng']));
    }
    var travel_path = new google.maps.Polyline({
	    path: city_coords, 
	    strokeColor: '#6600FF', 
	    strokeWeight: 2
	}); 
    travel_path.setMap(map); 
}

