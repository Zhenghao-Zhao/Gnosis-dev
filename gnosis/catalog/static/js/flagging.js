$(document).click(function (e) {
    var container = $(".popup");
    // if the target of the click isn't the container nor a descendant of the container
    if (!$(".more_vert").is(e.target) && container.has(e.target).length === 0) {
        container.attr('hidden', true);
    }
});

function toggle_more(ele) {
    var hidden = $(ele).siblings('.popup').attr('hidden');
    $('.popup').attr('hidden', true);
    $(ele).siblings('.popup').attr('hidden', !hidden);
}

function open_dialog(id, authenticated) {
    if (authenticated) {
        $('.popup').attr('hidden', true);
        $('.cover').attr('hidden', false);

        // add comment id to te form
        $("<input />").attr("type", "hidden")
            .attr("name", "comment_id")
            .attr("value", id)
            .appendTo("#flag_form");
    }else{

    }
}

function cancel_form() {
    $('#flag_form').trigger('reset');
    $('.popup').attr('hidden', true);
}

// jQuery plugin to prevent double submission of forms
jQuery.fn.preventDoubleSubmission = function () {
    $(this).on('submit', function (e) {
        var $form = $(this);

        if ($form.data('submitted')) {
            // Previously submitted - don't submit again
            e.preventDefault();
        } else {
            // Mark it so that the next submit can be ignored
            $form.data('submitted', true);
        }
    });

    // Keep chainability
    return this;
};

$('form').preventDoubleSubmission();