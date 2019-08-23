from django import forms
from django.utils.safestring import mark_safe


class ReCAPTCHA(forms.Widget):
    """
    Default reCAPTCHA v2 widget.
    (with "I'm not robot" checkbox)
    """

    def __init__(self, sitekey, name):
        """
        :param sitekey: site key (public key)
        """
        super(ReCAPTCHA, self).__init__()

        self.sitekey = sitekey
        self.name = name

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
        If field g-recaptcha-response is not empty, client-side verification is successful, otherwise not.
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
            '<br/><button class="g-recaptcha btn btn-primary btn-lg float-right" data-sitekey="%(sitekey)s"'
            ' data-callback="onSubmit" >'
            '%(name)s</button>' % {
                'name': self.name,
                'sitekey': self.sitekey
            }
        )
