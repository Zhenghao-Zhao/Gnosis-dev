from catalog.forms import PaperForm, PaperImportForm
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

    def test_clean_abstract(self):
        form = PaperForm()
        if form.is_valid():
            form.clean_abstract()
            self.assertTrue(form.fields['abstract'].label is None or form.fields['abstract'].label == 'abstract')

    def test_clean_keywords(self):
        form = PaperForm()
        if form.is_valid():
            form.clean_keywords()
            self.assertTrue(form.fields['keywords'].label is None or form.fields['keywords'].label == 'keywords')

    def test_clean_download_link(self):
        form = PaperForm()
        if form.is_valid():
            form.clean_download_link()
            self.assertTrue(form.fields['download_link'].label is None or form.fields['download_link'].label == 'download_link')

class PaperImportFormTest(TestCase):

    def test_clean_url(self):
        form = PaperImportForm()
        if form.is_valid():
            form.clean_url()
            self.assertTrue(form.fields['url'].label is None or form.fields['url'].label == 'url')
