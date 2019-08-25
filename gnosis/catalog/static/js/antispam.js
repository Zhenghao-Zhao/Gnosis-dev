function onSubmitPaper(token) {
    // trigger submit on a unique form
    document.getElementById("paper-form").submit();
}

function onSubmitComment(token) {
    // trigger submit on a unique form
    document.getElementById("comment-form").submit();
}

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







