$(document).ready(function(){
    map = new L.Map('map');

	// create the tile layer with correct attribution
	var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
	var osmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
	var osm = new L.TileLayer(osmUrl, {minZoom: 3, maxZoom: 12, attribution: osmAttrib});

	// start the map in Central Australia
	map.setView(new L.LatLng(-25.518615, 134.264176),3);
	map.addLayer(osm);

	//Prototype
	var canberra = L.circle([-35.295818, 149.117691], 50000, {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.5
    })
    canberra.on('click',function(){
        alert('You are correct, Grant is lame in all of these places, especially Canberra');
    })
    canberra.addTo(map);

    var wool = L.circle([-34.385121, 150.886490], 20000, {
        color: 'green',
        fillColor: 'light green',
        fillOpacity: 0.5
    })
    wool.addTo(map);

});
        
