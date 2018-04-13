$( document ).ready(function() {
  var current_page = window.location.href;
  var lst = current_page.split('/');
  var len_lst = lst.length;
  var book_id = lst[len_lst-1];
	$.ajax({
  		url: "/getMap",
  		data: {book_id: book_id, },
  		dataType: "json"
  	})
  	.done(function(data) {
    	console.log(data);
      createMap(data);
    })
	;

});

function createMap(data) {
  mapboxgl.accessToken = 'pk.eyJ1IjoiYW15eWh1YW5nIiwiYSI6ImNqZngwd2UxczN4N3gyd21kOWJoNzJyMGoifQ.TasyG6w1wCe8uSLibB4AWw';
  var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/basic-v9',
  });
  map.addControl(new mapboxgl.NavigationControl());

  for (entry in data) {
    var marker = new mapboxgl.Marker()
    .setLngLat(data[entry])
    .addTo(map);
  }

  if (data.length > 1) {

    map.on('load', function (data) {
    map.addLayer({
      "id": "route",
      "type": "line",
      "source": {
        "type": "geojson",
        "data": {
          "type": "Feature",
          "properties": {},
          "geometry": {
            "type": "LineString",
            "coordinates": [[30.5, 50.5],[5.5, 50.5]]
          }
        }
      },
      "layout": {
        "line-join": "round",
        "line-cap": "round"
      },
      "paint": {
        "line-color": "#888",
        "line-width": 8
      }
    });
  });
    
  } else {
    console.log("not longer than 1");
  }
}

                