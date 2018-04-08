
// $(document).on('click', '.delete', function() {
// 	var row = $(this).parent().parent();
// 	var tripname = row.children()[0].innerHTML;
// 	var destination = row.children()[1].innerHTML;
//     $.post('delete-trip', {tripname:tripname, destination:destination})
//     .done(function() {})
//     .fail(function() { alert("error"); })
// 	row.remove();
// });

// var count = 0;

// $(document).ready(
// 	$(".inspect").on('click', function() {
// 		if (count == 0) {
// 			addFrame();
// 			count = count + 1;
// 		}
// 		var row = $(this).parent().parent();
// 		var destination = row.children()[1].innerHTML;
// 		$('#iframecontent').empty();
// 		var secondString = '<iframe width="600" height="450" frameborder="0" style="border:0" src="https://www.google.com/maps/embed/v1/place?key=AIzaSyCBaUAaH88OX-p0kLtdp8Ap2bPs4X2RpTU&q=' + destination + '" allowfullscreen></iframe>';
// 		$('#iframecontent').append(secondString);
// 	}));


// function addFrame() {
// 	var stringToAppend = '<h1><b>Trip Details</b></h1><div id="iframecontent"></div>';
// 		$('#iframecontainer').append(stringToAppend);
// }
