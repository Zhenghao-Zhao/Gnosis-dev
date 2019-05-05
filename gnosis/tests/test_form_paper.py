from catalog.forms import PaperForm
from django.test import TestCase

# Create your tests here.
# To run this test, use command: py -3 manage.py test tests.test_form_paper
class PaperFormTest(TestCase):
    def test_fields(self):
        form = PaperForm()
        self.assertEquals(form.fields["title"].label, "Title*")
        self.assertEquals(form.fields["abstract"].label, "Abstract*")
        self.assertEquals(form.fields["keywords"].label, "Keywords")
        self.assertEquals(form.fields["download_link"].label, "Download Link*")

        for visible in form.visible_fields():
            self.assertEquals(visible.field.widget.attrs["class"], "form-control")

    def test_clean_title(self):
        form = PaperForm()
        if form.is_valid():
            form.clean_title()
            self.assertTrue(form.fields['title'].label is None or form.fields['title'].label == 'title')