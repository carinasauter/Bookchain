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


(function ($) {
    "use strict";

    
    /*==================================================================
    [ Validate ]*/
    var input = $('.validate-input .input100');

    $('.validate-form').on('submit',function(){
        var check = true;

        for(var i=0; i<input.length; i++) {
            if(validate(input[i]) == false){
                showValidate(input[i]);
                check=false;
            }
        }

        return check;
    });


    $('.validate-form .input100').each(function(){
        $(this).focus(function(){
           hideValidate(this);
        });
    });

    function validate (input) {
        if($(input).attr('type') == 'email' || $(input).attr('name') == 'email') {
            if($(input).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
                return false;
            }
        }
        else {
            if($(input).val().trim() == ''){
                return false;
            }
        }
    }

    function showValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).removeClass('alert-validate');
    }
    
    

})(jQuery);
