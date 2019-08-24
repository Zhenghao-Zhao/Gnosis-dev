from django import forms
from django.utils.safestring import mark_safe


class ReCAPTCHA(forms.Widget):
    """
    Default reCAPTCHA v2 widget.
    (with "I'm not robot" checkbox)
    """

    def __init__(self, sitekey, name, submitfun):
        """
        :param sitekey: site key (public key)
        """
        super(ReCAPTCHA, self).__init__()

        self.sitekey = sitekey
        self.name = name
        self.submitfun = submitfun

    def render(self, name, value, *args, **kwargs):
        """
        Returns this widget rendered as HTML.
        """
        return mark_safe(
            '<br/><div class="g-recaptcha" data-callback="dataCallback" data-expired-callback="dataExpiredCallback" '
            'data-error-callback="dataErrorCallback" data-sitekey="%(sitekey)s"></div>'
            '<input type="submit" class="btn btn-primary btn-lg float-right captcha-submit" value="%(name)s" disabled/>' % {
                'name': self.name,
                'sitekey': self.sitekey
            })

    def value_from_datadict(self, data, files, name):
        """
        Get the value of recaptcha, either has value in g-recaptcha-response or None
        """
        return data.get('g-recaptcha-response', None)


class InvisibleReCAPTCHA(ReCAPTCHA):
    """
    Invisible reCAPTCHA widget.
    """

    def render(self, name, value, *args, **kwargs):
        """
        Returns this widget rendered as HTML.
        """

        return mark_safe(
            '<br/><button class="g-recaptcha btn btn-primary btn-lg float-right captcha-submit" data-sitekey="%(sitekey)s"'
            ' data-callback="%(submitfun)s">'
            '%(name)s</button>' % {
                'name': self.name,
                'sitekey': self.sitekey,
                'submitfun': self.submitfun
            }
        )
