// $(document).ready(
//     var book_id = 6
// 	$.ajax({
// 		type: "GET",
// 		url: "/getMap",
// 		data: {book_id: book_id, },
// 		dataType: "json"
// 	})
// )

// $(document).on('click', '.registerThis', function() {
// 	var bookID = $(this).parent().parent().children()[0].innerHTML;
// 	callAPI(bookID, sendToBackend);
// })


$( document ).ready(function() {
    var book_id = 6;
	$.ajax({
  		url: "/getMap",
  		data: {book_id: book_id, },
  		dataType: "json"
  	})
  	.done(function(data) {
    	console.log(data);
    })
	;

});