var current_page = window.location.href;
var lst = current_page.split('/');
var len_lst = lst.length;
var book_id = lst[len_lst-1];

var currentuser;

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

$(document).on('click', '.addReview', function() {
  var current_page = window.location.href;
  var lst = current_page.split('/');
  var len_lst = lst.length;
  var book_id = lst[len_lst-1];
  var comment = $("#comment")[0];
  var content = comment['value'];
  $.ajax({
    type: "POST",
    url: "/addReview",
    data: {comment: content, book_id: book_id},
    dataType: "json"
  });
  $(".memberComments")
  .prepend('<p>"<i>' + content + '</i>"<br>- ' + currentuser + "</p>")
  .done($("#comment").val(''));
})




$(document).ready(function() {
  $('textarea').characterCounter();
});


$( "#1" ).hover(
  function() {
    $( this ).addClass( "amber-text" ).removeClass("grey-text lighten-1");

  }, function() {
    $( this ).removeClass( "amber-text").addClass("grey-text lighten-1");
  }
);

$( "#2" ).hover(
  function() {
    $( this ).addClass( "amber-text" ).removeClass("grey-text lighten-1");
    $("#1" ).addClass( "amber-text" ).removeClass("grey-text lighten-1");
  }, function() {
    $( this ).removeClass( "amber-text").addClass("grey-text lighten-1");
    $("#1" ).removeClass( "amber-text" ).addClass("grey-text lighten-1");
  }
);

$( "#3" ).hover(
  function() {
    $( this ).addClass( "amber-text" ).removeClass("grey-text lighten-1");
    $("#2" ).addClass( "amber-text" ).removeClass("grey-text lighten-1");
    $("#1" ).addClass( "amber-text" ).removeClass("grey-text lighten-1");
  }, function() {
    $( this ).removeClass( "amber-text").addClass("grey-text lighten-1");
    $("#2" ).removeClass( "amber-text" ).addClass("grey-text lighten-1");
    $("#1" ).removeClass( "amber-text" ).addClass("grey-text lighten-1");
  }
);
 
$( "#4" ).hover(
  function() {
    $( this ).addClass( "amber-text" ).removeClass("grey-text lighten-1");
    $("#3" ).addClass( "amber-text" ).removeClass("grey-text lighten-1");
    $("#2" ).addClass( "amber-text" ).removeClass("grey-text lighten-1");
    $("#1" ).addClass( "amber-text" ).removeClass("grey-text lighten-1");
  }, function() {
    $( this ).removeClass( "amber-text").addClass("grey-text lighten-1");
    $("#3" ).removeClass( "amber-text" ).addClass("grey-text lighten-1");
    $("#2" ).removeClass( "amber-text" ).addClass("grey-text lighten-1");
    $("#1" ).removeClass( "amber-text" ).addClass("grey-text lighten-1");
  }
);


$( "#5" ).hover(
  function() {
    $( this ).addClass( "amber-text" ).removeClass("grey-text lighten-1");
    $("#4" ).addClass( "amber-text" ).removeClass("grey-text lighten-1");
    $("#3" ).addClass( "amber-text" ).removeClass("grey-text lighten-1");
    $("#2" ).addClass( "amber-text" ).removeClass("grey-text lighten-1");
    $("#1" ).addClass( "amber-text" ).removeClass("grey-text lighten-1");
  }, function() {
    $( this ).removeClass( "amber-text").addClass("grey-text lighten-1");
    $("#4" ).removeClass( "amber-text" ).addClass("grey-text lighten-1");
    $("#3" ).removeClass( "amber-text" ).addClass("grey-text lighten-1");
    $("#2" ).removeClass( "amber-text" ).addClass("grey-text lighten-1");
    $("#1" ).removeClass( "amber-text" ).addClass("grey-text lighten-1");
  }
);


function disableClick() {
    $('.star').each(function() {
    this.style.pointerEvents = 'none';
  })
}

$(document).one('click', '#1', function() {
  $.ajax({
    type: "POST",
    url: "/addRating",
    data: {rating: 1, book_id: book_id},
    dataType: "json"
  })
  $("#1").addClass( "amber-text" );
  deactivateHover();
  disableClick();
})


$(document).one('click', '#2', function() {
  $.ajax({
    type: "POST",
    url: "/addRating",
    data: {rating: 2, book_id: book_id},
    dataType: "json"
  })
    $("#2").addClass( "amber-text" );
    $("#1").addClass( "amber-text" );
    deactivateHover();
    disableClick();
})

$(document).one('click', '#3', function() {
  $.ajax({
    type: "POST",
    url: "/addRating",
    data: {rating: 3, book_id: book_id},
    dataType: "json"
  })
    $("#3").addClass( "amber-text" );
    $("#2").addClass( "amber-text" );
    $("#1").addClass( "amber-text" );
    deactivateHover();
    disableClick();
})

$(document).one('click', '#4', function() {
  $.ajax({
    type: "POST",
    url: "/addRating",
    data: {rating: 4, book_id: book_id},
    dataType: "json"
  })
    $("#4").addClass( "amber-text" );
    $("#3").addClass( "amber-text" );
    $("#2").addClass( "amber-text" );
    $("#1").addClass( "amber-text" );
    deactivateHover();
    disableClick();
})


$(document).one('click', '#5', function() {
  $.ajax({
    type: "POST",
    url: "/addRating",
    data: {rating: 5, book_id: book_id},
    dataType: "json"
  })
   $("#5").addClass( "amber-text" );
    $("#4").addClass( "amber-text" );
    $("#3").addClass( "amber-text" );
    $("#2").addClass( "amber-text" );
    $("#1").addClass( "amber-text" );
    deactivateHover();
    disableClick();
})

function deactivateHover() {
  $(".star").unbind('mouseenter mouseleave');
}


$(document).on('click', '.requestBook', function() {
  $.ajax({
    type: "POST",
    url: "/requestBook",
    data: {book_id: book_id},
    dataType: "json"
  })
  $( this ).addClass(" disabled ").text("Requested");
})


  
$( document ).ready(function() {
	$.ajax({
  		url: "/getMap",
  		data: {book_id: book_id, },
  		dataType: "json"
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

                