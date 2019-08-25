from django import forms
from django.utils.safestring import mark_safe


class ReCAPTCHA(forms.Widget):
    """
    Default reCAPTCHA v2 widget.
    (with "I'm not robot" checkbox)
    """

    def __init__(self, widget_id):

        super(ReCAPTCHA, self).__init__()

        self.widget_id = widget_id

    def render(self, name, value, *args, **kwargs):
        """
        Returns this widget rendered as HTML.
        """
        return mark_safe(
            '<div id="%(id)s"></div> '
            '<script src="https://www.google.com/recaptcha/api.js?onload=onloadCallback&render=explicit" async defer></script>' % {
                'id': self.widget_id
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
            '<div id="%(id)s"></div> '
            '<script src="https://www.google.com/recaptcha/api.js?onload=onloadCallback&render=explicit" async defer></script>'
            % {
                'id': self.widget_id
            })