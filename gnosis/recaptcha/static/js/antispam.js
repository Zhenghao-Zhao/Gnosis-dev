/* callback functions for when different errors happen at client side verification */

// when receive data (meaning client side verification is successful), allow submit button to work properly.
function dataCallback() {
    $('.captcha-submit').removeAttr('disabled');
}

// the response token has 2 mins before it expires, when that happens, disable the submit button (requires to re-verify).
function dataExpiredCallback() {
    $('.captcha-submit').attr('disabled', true);
}

// if received connection error, use a pop up window to remind user to re-verify, also disables the submit button.
function dataErrorCallback() {
    $('.captcha-submit').attr('disabled', true);
    window.alert("Network connectivity error, please retry reCaptcha.")
}