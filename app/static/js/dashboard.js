// Get user data once the page loaded to create map for the logged in user
$(document).ready(function () {
    $.ajax({
        url: "/getUser",
        dataType: "json"
    })
        .done(function (data) {
            var username = data[0];
            currentuser = username;

            $.ajax({
                url: "/getMapForUser",
                data: { user: currentuser },
                dataType: "json"
            })
                .done(function (data) {
                    createMap(data);
                });
        });
});

// Create Map for users
function createMap(data) {
    mapboxgl.accessToken = 'pk.eyJ1IjoiYW15eWh1YW5nIiwiYSI6ImNqZngwd2UxczN4N3gyd21kOWJoNzJyMGoifQ.TasyG6w1wCe8uSLibB4AWw';
    var map = new mapboxgl.Map({
        container: 'mapMain',
        style: 'mapbox://styles/mapbox/basic-v9',
        center: [-100.50, 40],
        zoom: 3
    });
    map.addControl(new mapboxgl.NavigationControl());

    for (entry in data) {
        var marker = new mapboxgl.Marker()
            .setLngLat(data[entry])
            .addTo(map);
    }

    latlngs = []
    for (entry in data) {
        latlngs.push(data[entry])
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
                            "coordinates": latlngs
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

// Register events to cancel requests when users click 'cancel request' buttons
$(document).on('click', '#cancelRequest', function() {
    var book_id = $(this).parent().parent().children()[0].innerHTML;
    $.ajax({
      // type: "POST",
      url: "/cancelRequest",
      data: {book_id: book_id},
      dataType: "json"
    })
    $( this ).addClass(" disabled ");
    $(this).closest('tr').remove();

  })