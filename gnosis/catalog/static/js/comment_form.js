// Submit comment on submit

$(document).ready(function(){
    $('#comment-form').on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!");  // sanity check
        create_comment();
    });
});

function create_comment() {
    console.log("create post is working!") // sanity check
    console.log($('#comment_text').val())
    $.ajax({
        url : "create_comment/", // the endpoint
        type : "POST", // http method
        data : { the_post : $('#comment_text').val() }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $('#comment_text').val(''); // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};