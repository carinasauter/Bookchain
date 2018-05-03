// Register events to handle book requests. Request buttons will be disabled once users click 'request'.
$(document).ready(
    $(document).on('click', '.requestBook', function() {
        var bookID = $(this).attr("data-bookid");
        $.ajax({
            type: "POST",
            url: "/requestBook",
            data: {book_id: bookID},
            dataType: "json"
        })
    $( this ).addClass(" disabled ").removeClass(" requestBook ");
    $(this).html('Requested');
    })
)