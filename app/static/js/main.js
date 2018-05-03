var currentuser;
// Upon first click on finding a book to register the table header is created once and results
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
        var query = "?q=" + parseInput(user_input)
        callAPI(query, parseQuery);
    }),

    // Register events for available-switch to change book status between 'reading' and 'available'
    $(".available-checkbox").change(function (event) {
        bookID = String(this.id).replace("bookID-", "");
        status_cell = $(event.target).parent().parent().parent().prev().prev();
        if (this.checked) {
            $.ajax({
                type: "POST",
                contentType: "application/json",
                url: "/setBookAvailability",
                data: JSON.stringify({book: bookID, status: "available"}),
                dataType: "json"
            });
            status_cell = status_cell.html("available");
        }
        else {
            $.ajax({
                type: "POST",
                contentType: "application/json",
                url: "/setBookAvailability",
                data: JSON.stringify({book: bookID, status: "reading"}),
                dataType: "json"
            });
            status_cell = status_cell.html("reading");
        }
    }),

    // Register events for shipBook icons to send ajax request to update book status from 'requested' and 'shiping' 
    // and grey out the shipping icon
    $(".shipBook").click(function (event) {
        var bookID = $(this).parent().parent().children()[0].innerHTML;
        $.ajax({
            type: "POST",
            contentType: "application/json",
            url: "/shipBook",
            data: JSON.stringify({book: bookID}),
            dataType: "json"
        });
        $(this).addClass(" grey-text ");
    })
)



// Register events for registering the book from query 
$(document).on('click', '.registerThis', function() {
    var bookID = $(this).parent().parent().children()[0].innerHTML;
    $(this).addClass("disabled");
    $(this).html("Registered");
    callAPI("/" + bookID, sendToBackend);
})

// Register events for key up event when users press 'Enter'
$("#search_query").keyup(function(event) {
    if (event.keyCode === 13) {
        $("#registerBook").click();
    }
});

// Add pointer into mourse's cursor when users hover on the icons 
$(document).on('mouseover', '.removebook', function() {
    $( this ).css( 'cursor', 'pointer' );
})

$(document).on('mouseover', '.bookdetails', function() {
    $( this ).css( 'cursor', 'pointer' );
})
$(document).on('mouseover', '#cancelRequest', function() {
    $( this ).css( 'cursor', 'pointer' );
})
$(document).on('mouseover', '.labelprint', function() {
    $( this ).css( 'cursor', 'pointer' );
})
$(document).on('mouseover', '.shipBook', function() {
    $( this ).css( 'cursor', 'pointer' );
})

// Function when user clicks "Received Book"
$(document).on('click', '#receive-book', function() {
    var bookID = $(this).parent().parent().children()[0].innerHTML;
    $(this).closest('tr').remove();
         $.ajax({
             url: "/receiveBook",
             data: {bookID: bookID},
         })
         .done(function(){
            location.reload();
         });
});

// When "details" button is clicked in the booksincirc page, generates the book page
$(document).on('click', '.bookdetails', function() {
    var bookID = $(this).attr("data-bookid");
    var url = "/book/" + bookID;
    window.open(url,"_self");
})

// When "remove" button is clicked in the dashboard, removes the book from the database
$(document).on('click', '.removebook', function() {
    var r = confirm("Remove book from bookchain?");
    if (r == true) {
        var bookID = $(this).parent().parent().children()[0].innerHTML;
        $.ajax({
            url: "/removeBook",
            data: {book_id: bookID},
            type: "POST",
            dataType: "json",
        })
        // remove the book from the html
        $(this).closest('tr').remove();
        // pop up message to confirm removal
        alert("Successfully removed from circulation.");
        var result = $("#borrowedAndContributed").children().children('tr').children('td.hidden');
        for (entry of result) {
            if (entry.innerHTML == bookID) {
                entry.closest('tr').remove();
            }
        }
    } else {
        return;
    }

})

// Composing information and sending to backend
function sendToBackend(data) {
    var bookInfo = data['volumeInfo'];
    var title = bookInfo['title'];
    var author = bookInfo['authors'];

    var thumbnail = bookInfo['imageLinks'];
    if (typeof thumbnail != 'undefined') {
        thumbnail = thumbnail['large'];
        thumbnail_small = bookInfo['imageLinks']['thumbnail'];
        if (typeof thumbnail == 'undefined') {
            thumbnail = bookInfo['imageLinks']['thumbnail'];
            thumbnail_small = bookInfo['imageLinks']['thumbnail'];
        }
    } else {
        thumbnail = "static/img/noImgFound.jpg";
        thumbnail_small = "static/img/noImgFound.jpg";
    }

    if (typeof author != 'undefined') {
        author = author[0];
    } else {
        author = "not available"
    }
    var short_description = bookInfo['description'];
    if (typeof short_description != 'undefined') {
    } else {
        short_description = "no description available.";
    }
    var isbn = bookInfo['industryIdentifiers'];
    if (typeof isbn != 'undefined') {
        isbn1 = isbn[0]['type'];
        if (isbn1 == 'ISBN_10') {
            isbn2 = isbn[1];
            if (typeof isbn2 !='undefined') {
                isbn = isbn[1]['identifier'];
            } else {
                isbn = isbn[0]['identifier'];
            }
        } else {
            isbn = isbn[0]['identifier'];
        }
    } else {
        isbn = "";
    }
    $.ajax({
        type: "POST",
        url: "/registerBook",
        data: { title: title, author: author, thumbnail: thumbnail, thumbnail_small: thumbnail_small, short_description: short_description, isbn: isbn},
        dataType: "json",
    }).done(function( o ) {
    });
}


// Event hander for calling the Google Books API using the user's search query to aid registering a book
function callAPI(query, whatToDo) {
    $.get("https://www.googleapis.com/books/v1/volumes" + query,
        function(data) {
            whatToDo(data);
        },'json'
    );
}


// Helper function to add the table header once.
function addTableHeader() {
    $("#results").append('<div class="row"><div id="tableHeader" class="col s12 m12 l12">SEARCH RESULTS\
    </div></div><div id="searchResults"></div>');
}


// Parsing the results from the Google Books API and injecting first 20 to HTML
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
        } else {
            short_description = "no description available.";
        }

        var thumbnail = bookInfo['imageLinks'];
        if (typeof thumbnail != 'undefined') {
            thumbnail = thumbnail['thumbnail'];
        } else {
            thumbnail = "static/img/noImgFound.jpg";
        }
        var stringToAppend = "<div class = 'row card horizontal s12 m12 l10 offset-l1 valign-wrapper'>\
        <p class= 'hidden'>" + bookID + "</p><div class='col s3 m2 l2'><img src='" + thumbnail + "' alt='coverThumbnail onerror='imgError(this)'>\
        </div><div class='col s5 m7 l8 left-align'><p><b>" + title + "</b></p><p>\
        " + author + "</p><p class = 'line-clamp hide-on-small-only'>" + short_description + "</p></div><div class='col s4 m3 l2'><button \
        class='btn waves-effect waves-light registerThis' type='text'>Register</button></div></div></div>"
        $("#searchResults").append(stringToAppend);
        var texts = document.getElementsByClassName('line-clamp');
        var len_texts = texts.length;
        var module = texts[len_texts-1];
        $clamp(module, {clamp: 3});
    }
}

// Parsing the results from the Google Books API and injecting first 20 to HTML
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

// Replace image if cover art not found
function imgError(image) {
    image.onerror = "";
    image.src = "/static/img/noImgFound.jpg";
    return true;
}

// Register events to print shipping label and open the label in the new window
$(document).on('click', '.labelprint', function() {
    var bookID = $(this).parent().parent().children()[0].innerHTML;
    $.ajax({
        url: "/printLabel",
        data: {book: bookID},
        dataType: "json"
    })
    .done(function(data) {
        openInNewTab(data);
    });
})

function openInNewTab(url) {
  var win = window.open(url, '_blank');
}




// Searches the circulation page for matching titles or authors, dynamically filters results
function searchCirc(event) {
    // Declare variables
    var input = document.getElementById('circQuery').value.toLowerCase();
    var bookList = document.getElementsByClassName('card horizontal')

    // Loop through all books, and hide those who don't match the search query
    for (i = 0; i < bookList.length; i++) {
        title = bookList[i].getElementsByTagName("b")[0].innerHTML.toLowerCase();
        author = bookList[i].getElementsByTagName("i")[0].innerHTML.toLowerCase();
        if (title.indexOf(input) > -1 || author.indexOf(input) > -1) {
            bookList[i].style.display = "";
        } else {
            bookList[i].style.display = "none";
        }
    }
}

