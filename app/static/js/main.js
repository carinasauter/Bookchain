// upon first click of submit the search result and playlist columns are created
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
    	console.log(query);
    	callAPI(query);
    })
)

// upon
$(document).on('click', '.registerThis', function() {
	console.log("You want to register this book.");
	var book_id = $(this).parent().parent();
	console.log(book_id);
})
    // check which column they are part of
    // var parent_id = $(this).parent().parent()[0].id;
    // console.log(parent_id);
    // var completedItem = $(this).parent();


// Event hander for calling the Google Books API using the user's search query to aid registering a book
function callAPI(query) {
	$.get("https://www.googleapis.com/books/v1/volumes?q=" + query,
		function(data) {
			console.log(data);
			parseQuery(data);
		},'json'
	);
}


function addTableHeader() {
	$("#results").append('<div class="row"><div id="tableHeader" class="col s12 m12 l12">Search Results\
    </div></div><div id="searchResults"></div>');
}


// parsing the results from the Google Books API and injecting first 20 to HTML
function parseQuery(data) {
	data = data['items'];
	var num_books = data.length;
	console.log(num_books);
	var firstBook = data[0];
	var bookInfo = firstBook['volumeInfo'];
	// var user_input = $('#searchbar').val();

	for (i = 0; i < 10; i++) {
		var currentBook = data[i];
		console.log(currentBook);
		var bookInfo = currentBook['volumeInfo'];
		var title = bookInfo['title'];
		var author = bookInfo['authors'];
		if (typeof author != 'undefined') {
			author = author[0];
		} else {
			author = "not available"
		}
		var isbn13 = bookInfo['industryIdentifiers'];
		if (typeof isbn13 != 'undefined') {
			isbn13 = isbn13[1];
			if (typeof isbn13 != "undefined") {
				isbn13 = isbn13['identifier'];
			}
		} else {
			isbn13 = 'not available';
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
		console.log(title, author, thumbnail);
		var stringToAppend = "<div class = 'row card horizontal s12 m12 l12 valign-wrapper'>\
		<div class='col s3 m3 l2'><p class= 'hidden'>" + isbn13 + "</p><img src='" + thumbnail + "' alt='coverThumbnail onerror='imgError(this)'>\
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


