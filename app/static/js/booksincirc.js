$(document).ready(
    $(document).on('click', '.requestBook', function() {
        console.log("requested book");

        var bookID = $(this).attr("data-bookid");
        $.ajax({
            type: "POST",
            url: "/requestBook",
            data: {book_id: bookID},
            dataType: "json"
        })
    $( this ).addClass(" grey-text ").removeClass(" requestBook ");
    $(this).html('Requested');
    })
)