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
};