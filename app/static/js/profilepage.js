var currentuser;
var current_page = window.location.href;
var lst = current_page.split('/');
var len_lst = lst.length;
var lookedAtUser = lst[len_lst-1];


$( document ).ready(function() {
  $.ajax({
      url: "/getUser",
      dataType: "json"
    })
    .done(function(data) {
      var username = data[0];
      currentuser = username;
    });
});


$( document ).ready(function() {
	$.ajax({
  		url: "/getMapForUser",
  		dataType: "json", 
  		data: {user: lookedAtUser}
  	})
  	.done(function(data) {
    	console.log(data);
      createMap(data);
    });
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
}