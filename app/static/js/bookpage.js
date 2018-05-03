// Below variables storing current user and book's data
var current_page = window.location.href;
var lst = current_page.split('/');
var len_lst = lst.length;
var book_id = lst[len_lst - 1];

var currentuser;


$(document).ready(function () {
  // Get user data once the page loaded
  $.ajax({
    url: "/getUser",
    dataType: "json"
  })
    .done(function (data) {
      var username = data[0];
      currentuser = username;
    });

  // Setup character counter in text area
  $('textarea').characterCounter();

  // Create map
  $.ajax({
    url: "/getMap",
    data: { book_id: book_id, },
    dataType: "json"
  })
    .done(function (data) {
      createMap(data);
    });
});

// Handle book requests events and disable the 'request' button after the current user click it
$(document).on('click', '.requestBook', function () {
  $.ajax({
    type: "POST",
    url: "/requestBook",
    data: { book_id: book_id },
    dataType: "json"
  })
  $(this).addClass(" disabled ").text("Requested");
})

// Handle cancel book requests events and disable the 'cancel request' button after the current user click it
$(document).on('click', '#cancelRequest', function () {
  $.ajax({
    // type: "POST",
    url: "/cancelRequest",
    data: { book_id: book_id },
    dataType: "json"
  })
  $(this).addClass(" disabled ").text("Request Cancelled");
})

// Register events to handle 'add review'
$(document).on('click', '.addReview', function () {
  var current_page = window.location.href;
  var lst = current_page.split('/');
  var len_lst = lst.length;
  var book_id = lst[len_lst - 1];
  var comment = $("#comment")[0];
  var content = comment['value'];
  $.ajax({
    type: "POST",
    url: "/addReview",
    data: { comment: content, book_id: book_id },
    dataType: "json"
  });
  $(".memberComments")
    .prepend('<p>"<i>' + content + '</i>"<br>- ' + currentuser + "</p>")
    .done($("#comment").val(''));
})

// Register hover events for changing color of star ratings
$("#1").hover(
  function () {
    $(this).addClass("amber-text").removeClass("grey-text lighten-1");
    $(this).css('cursor', 'pointer');

  }, function () {
    $(this).removeClass("amber-text").addClass("grey-text lighten-1");
  }
);

$("#2").hover(
  function () {
    $(this).addClass("amber-text").removeClass("grey-text lighten-1");
    $("#1").addClass("amber-text").removeClass("grey-text lighten-1");
    $(this).css('cursor', 'pointer');
  }, function () {
    $(this).removeClass("amber-text").addClass("grey-text lighten-1");
    $("#1").removeClass("amber-text").addClass("grey-text lighten-1");
  }
);

$("#3").hover(
  function () {
    $(this).addClass("amber-text").removeClass("grey-text lighten-1");
    $("#2").addClass("amber-text").removeClass("grey-text lighten-1");
    $("#1").addClass("amber-text").removeClass("grey-text lighten-1");
    $(this).css('cursor', 'pointer');
  }, function () {
    $(this).removeClass("amber-text").addClass("grey-text lighten-1");
    $("#2").removeClass("amber-text").addClass("grey-text lighten-1");
    $("#1").removeClass("amber-text").addClass("grey-text lighten-1");
  }
);

$("#4").hover(
  function () {
    $(this).addClass("amber-text").removeClass("grey-text lighten-1");
    $("#3").addClass("amber-text").removeClass("grey-text lighten-1");
    $("#2").addClass("amber-text").removeClass("grey-text lighten-1");
    $("#1").addClass("amber-text").removeClass("grey-text lighten-1");
    $(this).css('cursor', 'pointer');
  }, function () {
    $(this).removeClass("amber-text").addClass("grey-text lighten-1");
    $("#3").removeClass("amber-text").addClass("grey-text lighten-1");
    $("#2").removeClass("amber-text").addClass("grey-text lighten-1");
    $("#1").removeClass("amber-text").addClass("grey-text lighten-1");
  }
);


$("#5").hover(
  function () {
    $(this).addClass("amber-text").removeClass("grey-text lighten-1");
    $("#4").addClass("amber-text").removeClass("grey-text lighten-1");
    $("#3").addClass("amber-text").removeClass("grey-text lighten-1");
    $("#2").addClass("amber-text").removeClass("grey-text lighten-1");
    $("#1").addClass("amber-text").removeClass("grey-text lighten-1");
    $(this).css('cursor', 'pointer');
  }, function () {
    $(this).removeClass("amber-text").addClass("grey-text lighten-1");
    $("#4").removeClass("amber-text").addClass("grey-text lighten-1");
    $("#3").removeClass("amber-text").addClass("grey-text lighten-1");
    $("#2").removeClass("amber-text").addClass("grey-text lighten-1");
    $("#1").removeClass("amber-text").addClass("grey-text lighten-1");
  }
);

// Setup color of star ratings once the current user click the rating they want
$(document).one('click', '#1', function () {
  $.ajax({
    type: "POST",
    url: "/addRating",
    data: { rating: 1, book_id: book_id },
    dataType: "json"
  })
  $("#1").addClass("amber-text");
  deactivateHover();
  disableClick();
  updateRating();
})


$(document).one('click', '#2', function () {
  $.ajax({
    type: "POST",
    url: "/addRating",
    data: { rating: 2, book_id: book_id },
    dataType: "json"
  })
  $("#2").addClass("amber-text");
  $("#1").addClass("amber-text");
  deactivateHover();
  disableClick();
  updateRating();
})

$(document).one('click', '#3', function () {
  $.ajax({
    type: "POST",
    url: "/addRating",
    data: { rating: 3, book_id: book_id },
    dataType: "json"
  })
  $("#3").addClass("amber-text");
  $("#2").addClass("amber-text");
  $("#1").addClass("amber-text");
  deactivateHover();
  disableClick();
  updateRating();
})

$(document).one('click', '#4', function () {
  $.ajax({
    type: "POST",
    url: "/addRating",
    data: { rating: 4, book_id: book_id },
    dataType: "json"
  })
  $("#4").addClass("amber-text");
  $("#3").addClass("amber-text");
  $("#2").addClass("amber-text");
  $("#1").addClass("amber-text");
  deactivateHover();
  disableClick();
  updateRating();
})


$(document).one('click', '#5', function () {
  $.ajax({
    type: "POST",
    url: "/addRating",
    data: { rating: 5, book_id: book_id },
    dataType: "json"
  })
  $("#5").addClass("amber-text");
  $("#4").addClass("amber-text");
  $("#3").addClass("amber-text");
  $("#2").addClass("amber-text");
  $("#1").addClass("amber-text");
  deactivateHover();
  disableClick();
  updateRating();
})


function deactivateHover() {
  $(".star").unbind('mouseenter mouseleave');
}

// Once the rating is given by the current user, stop changing color of star ratings
function disableClick() {
  $('.star').each(function () {
    this.style.pointerEvents = 'none';
  })
}

function updateRating() {
  $.ajax({
    url: "/getRating",
    data: { book_id: book_id, },
    dataType: "json"
  }).done(function (data) {
    console.log(data[0]);
    console.log($("#averageRating"));
    $("#averageRating")[0].innerHTML = data[0];
  });
}

function createMap(data) {
  mapboxgl.accessToken = 'pk.eyJ1IjoiYW15eWh1YW5nIiwiYSI6ImNqZngwd2UxczN4N3gyd21kOWJoNzJyMGoifQ.TasyG6w1wCe8uSLibB4AWw';
  var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/basic-v9',
    center: [-100.50, 40],
    zoom: 3
  });
  map.addControl(new mapboxgl.NavigationControl());

  for (entry in data) {
    var marker = new mapboxgl.Marker()
      .setLngLat(data[entry])
      .addTo(map);
    // console.log(data[entry])
  }

  latlngs = []
  for (entry in data) {
    latlngs.push(data[entry])
  }
  console.log(latlngs)

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

