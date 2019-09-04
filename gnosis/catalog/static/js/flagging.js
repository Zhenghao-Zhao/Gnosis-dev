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

function open_dialog() {
    $('.popup').attr('hidden', true);
    $('.cover').attr('hidden', false).css({
        "background-color": "grey",
        "opacity": 0.5,

    })
}