/************** click anywhere on page to cancel popups **************/
$(document).click(function (e) {
    var container = $(".popup");
    // if the target of the click isn't the container nor a descendant of the container.
    if (!$(".more_vert").is(e.target) && container.has(e.target).length === 0) {
        container.attr('hidden', true);
    }
});

var this_flag_url;
var this_comment;

/************** opens flag dialog that contains flag form **************/

$('.open_flag_dialog').click(function () {
    // hide all current popups
    $('.popup').attr('hidden', true);
    $('#flag_form_container').attr('hidden', false);

    this_flag_url = $(this).attr('data-url');
    this_comment = $(this).closest('#comment_thread');
});

/************** hide popup form and reset its text. **************/
function cancel_form() {
    $('#flag_form').trigger('reset');
    $('.popup').attr('hidden', true);
}

/************** toggles more button: shows/hides popup menu **************/
$('.more_vert').click(function () {
    var hidden = $(this).siblings('.popup').attr('hidden');
    $('.popup').attr('hidden', true);
    $(this).siblings('.popup').attr('hidden', !hidden);
});

// points to the comment that has been flagged/hidden
$('.async-hide').click(function (e) {
    e.preventDefault();
    var url = $(this).attr('href');
    this_comment = $(this).closest('#comment_thread');
    $.ajax({
        type: 'POST',
        url: url,
        success: function (data) {
            console.log("submit successful!");
            if (this_comment != null) {
                $(this_comment).attr('hidden', true);
                $(this_comment).prevAll('#hidden_comment:first').attr('hidden', false);
            }
        },
        error: function (data) {
            alert("An error has occurred, please resubmit report.");
        },
    })
});

$('.unhide_comment').click(function (e) {
    e.preventDefault();
    var $hidden = $(this).closest('#hidden_comment');
    this_comment = $hidden.nextAll('#comment_thread:first');

    $.ajax({
        type: 'GET',
        url: $(this).attr('href'),
        success: function (data) {
            console.log("submit successful!");
            if (this_comment != null) {
                $hidden.attr('hidden', true);
                $(this_comment).attr('hidden', false);
            }
        },
        error: function (data) {
            alert("An error has occurred, please resubmit report.");
        },
    })
});

/************** click to show reported comment **************/
$('.show_comment').click(function (e) {
    e.preventDefault();
    var $hidden = $(this).closest('#reported_comment');
    this_comment = $hidden.nextAll('#comment_thread:first');
    console.log($(this).attr('href'));
    $.ajax({
        type: 'GET',
        url: $(this).attr('href'),
        success: function (data) {
            if (this_comment != null) {
                $hidden.attr('hidden', true);
                $(this_comment).attr('hidden', false);
            }
        },
        error: function (data) {
            alert('Request failed.')
        }
    })
});

/************** sending ajax post request with flag forms **************/
var form = $('#flag_form');
form.submit(function (e) {
    e.preventDefault();

    $('.popup').attr('hidden', true);
    // open loader
    $('#loader').attr('hidden', false);

    if (this_flag_url != null) {
        $.ajax({
            type: 'POST',
            url: this_flag_url,
            data: form.serialize(),
            success: function (data) {
                console.log("submit successful!");
                if (this_comment != null) {
                    $(this_comment).attr('hidden', true);
                    $(this_comment).prevAll('#reported_comment:first').attr('hidden', false);
                }
                $('#flag_form').trigger('reset');
                // close loader
                $('#loader').attr('hidden', true);
                $('#flag_response').attr('hidden', false);
            },
            error: function (data) {
                $('#loader').attr('hidden', true);
                alert("Request failed.");
            },

        })
    } else {
        alert("Undefined comment id.");
    }
});