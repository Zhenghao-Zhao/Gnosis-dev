function dataCallback() {
    $('.captcha-submit').removeAttr('disabled');
}

function dataExpiredCallback() {
    $('.captcha-submit').attr('disabled', true);
}

function dataErrorCallback() {
    $('.captcha-submit').attr('disabled', true);
    window.alert("Network connectivity error, please retry reCaptcha.")
}

function onSubmit(token) {
    document.getElementById("comment-form").submit();
}



