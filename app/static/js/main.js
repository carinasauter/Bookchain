// upon first click on finding a book to register the table header is created once and results
// are rendered every time. Also header is removed.
$(document).ready(
	$("#registerBook").one('click', function() {
		addTableHeader();
	}),
    $("#registerBook").on('click', function() {
    	$('#searchResults').empty();
    	$("#header").remove();
    	var user_input = $('#search_query').val();
    	$('#search_query').val("");
    	var query = parseInput(user_input)
    	callAPI(query, parseQuery);
    })
)


$(document).on('click', '.registerThis', function() {
	var bookID = $(this).parent().parent().children()[0].innerHTML;
	callAPI(bookID, sendToBackend);
})

function sendToBackend(data) {
	data = data['items'][0];
	var bookInfo = data['volumeInfo'];
	var title = bookInfo['title'];
	var author = bookInfo['authors'];
	var thumbnail = bookInfo['imageLinks'];
	if (typeof thumbnail != 'undefined') {
		thumbnail = thumbnail['smallThumbnail'];
	} else {
		thumbnail = "static/img/noImgFound.jpg";
	}
	if (typeof author != 'undefined') {
		author = author[0];
	} else {
		author = "not available"
	}
	var short_description = bookInfo['description'];
	if (typeof short_description != 'undefined') {
		short_description = short_description.substring(0, 300) + "...";
	} else {
		short_description = "no description available.";
	}
	$.ajax({
		type: "POST",
		url: "/registerBook",
		data: { title: title, author: author, thumbnail: thumbnail, short_description: short_description},
		dataType: "json",
	}).done(function( o ) {
		console.log('done!')
	});
}



// Event hander for calling the Google Books API using the user's search query to aid registering a book
function callAPI(query, whatToDo) {
	$.get("https://www.googleapis.com/books/v1/volumes?q=" + query,
		function(data) {
			whatToDo(data);
		},'json'
	);
}


// helper function to add the table header once.
function addTableHeader() {
	$("#results").append('<div class="row"><div id="tableHeader" class="col s12 m12 l12">Search Results\
    </div></div><div id="searchResults"></div>');
}


// parsing the results from the Google Books API and injecting first 20 to HTML
function parseQuery(data) {
	data = data['items'];
	var num_books = data.length;
	var firstBook = data[0];
	var bookInfo = firstBook['volumeInfo'];

	for (i = 0; i < 10; i++) {
		var currentBook = data[i];
		var bookInfo = currentBook['volumeInfo'];
		var title = bookInfo['title'];
		var author = bookInfo['authors'];
		var bookID = currentBook['id'];
		if (typeof author != 'undefined') {
			author = author[0];
		} else {
			author = "not available"
		}
		var short_description = bookInfo['description'];
		if (typeof short_description != 'undefined') {
			short_description = short_description.substring(0, 300) + "...";
		} else {
			short_description = "no description available.";
		}

		var thumbnail = bookInfo['imageLinks'];
		if (typeof thumbnail != 'undefined') {
			thumbnail = thumbnail['smallThumbnail'];
		} else {
			thumbnail = "static/img/noImgFound.jpg"; 
		}
		var stringToAppend = "<div class = 'row card horizontal s12 m12 l12 valign-wrapper'>\
		<p class= 'hidden'>" + bookID + "</p><div class='col s3 m3 l2'><img src='" + thumbnail + "' alt='coverThumbnail onerror='imgError(this)'>\
		</div><div class='col card-content s4 m4 l8 left-align'><p><b>" + title + "</b></p><p>\
		// " + author + "</p><p id='short'>" + short_description + "</p></div><div class='col s4 m4 l2'><button \
		class='btn registerThis' type='text'>Register</button></div></div></div>"
		$("#searchResults").append(stringToAppend);
	}
}

// parsing the results from the Google Books API and injecting first 20 to HTML
function parseInput(data) {
	var output = ""
	var getParts = data.split(" ");
	var length = getParts.length;
	for (i = 0; i < length; i++) {
		output += getParts[i] + "+";
	}
	output = output.substring(0, output.length - 1);
	return output
}

// replace image if cover art not found
function imgError(image) {
    image.onerror = "";
    image.src = "/static/img/noImgFound.jpg";
    return true;
}


$(document).on('click', '.labelprint', function() {
	var requester = "Amy";
	$.ajax({
		type: "POST",
		url: "/printLabel",
		data: {requester: requester, },
		dataType: "json"
	})
})



function openInNewTab(url) {
  var win = window.open(url, '_blank');
  win.focus();
}


