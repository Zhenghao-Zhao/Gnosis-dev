function dataCallback() {
    $('.captcha-submit').removeAttr('disabled');
}

function dataExpiredCallback() {
    $('.captcha-submit').attr('disabled', true);
}