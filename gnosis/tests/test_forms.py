from catalog.forms import PaperForm, PaperImportForm, PersonForm, DatasetForm, VenueForm, CommentForm, CodeForm, \
    SearchVenuesForm, SearchDatasetsForm, SearchPapersForm, SearchPeopleForm, SearchCodesForm
from django.test import TestCase

# Create your tests here.
# To run this test, use command: py -3 manage.py test tests.test_form_paper


#
# Search forms test
#
class SearchVenuesFormTest(TestCase):

    def test_fields(self):
        form = SearchVenuesForm()
        for visible in form.visible_fields():
            self.assertEquals(visible.field.widget.attrs["class"], "form-control")

    def test_clean_venue_name(self):
        form = SearchVenuesForm()
        if form.is_valid():
            form.clean_venue_name()
            self.assertTrue(form.fields['venue_name'].label is None or form.fields['venue_name'].label == 'venue_name')

    def test_clean_venue_publication_year(self):
        form = SearchVenuesForm()
        if form.is_valid():
            form.clean_venue_publication_year()
            self.assertTrue(form.fields['venue_publication_year'].label is None or form.fields['venue_publication_year'].label == 'venue_publication_year')

class SearchDatasetsFormTest(TestCase):

    def test_fields(self):
        form = SearchDatasetsForm()
        self.assertEquals(form.fields["name"].label, "Name")
        self.assertEquals(form.fields["keywords"].label, "Keyword (single keyword, e.g. network, computer vision)*")

        for visible in form.visible_fields():
            self.assertEquals(visible.field.widget.attrs["class"], "form-control")

    def test_clean_name(self):
        form = SearchDatasetsForm()
        if form.is_valid():
            form.clean_name()
            self.assertTrue(form.fields['name'].label is None or form.fields['name'].label == 'name')

    def test_clean_keywords(self):
        form = SearchDatasetsForm()
        if form.is_valid():
            form.clean_name()
            self.assertTrue(form.fields['keywords'].label is None or form.fields['keywords'].label == 'keywords')

class SearchPapersFormTest(TestCase):

    def test_fields(self):
        form = SearchPapersForm()
        for visible in form.visible_fields():
            self.assertEquals(visible.field.widget.attrs["class"], "form-control")

    def test_clean_paper_title(self):
        form = SearchPapersForm()
        if form.is_valid():
            form.clean_paper_title()
            self.assertTrue(form.fields['paper_title'].label is None or form.fields['paper_title'].label == 'paper_title')


class SearchPeopleFormTest(TestCase):

    def test_fields(self):
        form = SearchPeopleForm()
        for visible in form.visible_fields():
            self.assertEquals(visible.field.widget.attrs["class"], "form-control")

    def test_clean_person_name(self):
        form = SearchPeopleForm()
        if form.is_valid():
            form.clean_person_name()
            self.assertTrue(form.fields['person_name'].label is None or form.fields['person_name'].label == 'person_name')


class SearchCodesFormTest(TestCase):

    def test_fields(self):
        form = SearchCodesForm()
        self.assertEquals(form.fields["keywords"].label, "Keywords (e.g. GCN, network, computer vision)")

        for visible in form.visible_fields():
            self.assertEquals(visible.field.widget.attrs["class"], "form-control")

    def test_clean_keywords(self):
        form = SearchCodesForm()
        if form.is_valid():
            form.clean_keywords()
            self.assertTrue(
                form.fields['keywords'].label is None or form.fields['keywords'].label == 'keywords')


#
# Model forms test
#

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

class PersonFormTest(TestCase):

    def test_fields(self):
        form = PersonForm()
        self.assertEquals(form.fields["first_name"].label, "First Name*")
        self.assertEquals(form.fields["middle_name"].label, "Middle Name")
        self.assertEquals(form.fields["last_name"].label, "Last Name*")
        self.assertEquals(form.fields["affiliation"].label, "Affiliation")
        self.assertEquals(form.fields["website"].label, "Website")

        for visible in form.visible_fields():
            self.assertEquals(visible.field.widget.attrs["class"], "form-control")
            self.assertEquals(visible.field.widget.attrs.update({"style": "width:25em"}))

    def test_clean_first_name(self):
        form = PersonForm()
        if form.is_valid():
            form.clean_first_name()
            self.assertTrue(form.fields['first_name'].label is None or form.fields['first_name'].label == 'first_name')

    def test_clean_middle_name(self):
        form = PersonForm()
        if form.is_valid():
            form.clean_middle_name()
            self.assertTrue(form.fields['middle_name'].label is None or form.fields['middle_name'].label == 'middle_name')

    def test_clean_last_name(self):
        form = PersonForm()
        if form.is_valid():
            form.clean_last_name()
            self.assertTrue(form.fields['last_name'].label is None or form.fields['last_name'].label == 'last_name')

    def test_clean_affiliation(self):
        form = PersonForm()
        if form.is_valid():
            form.clean_affiliation()
            self.assertTrue(form.fields['affiliation'].label is None or form.fields['affiliation'].label == 'affiliation')

    def test_clean_website(self):
        form = PersonForm()
        if form.is_valid():
            form.clean_website()
            self.assertTrue(form.fields['website'].label is None or form.fields['website'].label == 'website')

class DatasetFormTest(TestCase):

    def test_fields(self):
        form = DatasetForm()
        self.assertEquals(form.fields["name"].label, "Name*")
        self.assertEquals(form.fields["keywords"].label, "Keywords*")
        self.assertEquals(form.fields["description"].label, "Description*")
        self.assertEquals(form.fields["source_type"].label, "Type*")
        self.assertEquals(form.fields["publication_date"].label, "Publication Date (yyyy-mm-dd)")
        self.assertEquals(form.fields["website"].label, "Website")

        for visible in form.visible_fields():
            self.assertEquals(visible.field.widget.attrs["class"], "form-control")
            self.assertEquals(visible.field.widget.attrs.update({"style": "width:25em"}))

    def test_clean_name(self):
        form = DatasetForm()
        if form.is_valid():
            form.clean_name()
            self.assertTrue(form.fields['name'].label is None or form.fields['name'].label == 'name')

    def test_clean_keywords(self):
        form = DatasetForm()
        if form.is_valid():
            form.clean_keywords()
            self.assertTrue(form.fields['keywords'].label is None or form.fields['keywords'].label == 'keywords')

    def test_clean_description(self):
        form = DatasetForm()
        if form.is_valid():
            form.clean_description()
            self.assertTrue(form.fields['description'].label is None or form.fields['description'].label == 'description')

    def test_clean_source_type(self):
        form = DatasetForm()
        if form.is_valid():
            form.clean_source_type()
            self.assertTrue(form.fields['source_type'].label is None or form.fields['source_type'].label == 'source_type')

    def test_clean_publication_date(self):
        form = DatasetForm()
        if form.is_valid():
            form.clean_publication_date()
            self.assertTrue(form.fields['publication_date'].label is None or form.fields['publication_date'].label == 'publication_date')

    def test_clean_website(self):
        form = DatasetForm()
        if form.is_valid():
            form.clean_website()
            self.assertTrue(form.fields['website'].label is None or form.fields['website'].label == 'website')

class VenueFormTest(TestCase):

    def test_fields(self):
        form = VenueForm()
        self.assertEquals(form.fields["name"].label, "Name*")
        self.assertEquals(form.fields["publisher"].label, "Publisher*")
        self.assertEquals(form.fields["publication_date"].label, "Publication Date (yyyy-mm-dd)*")
        self.assertEquals(form.fields["source_type"].label, "Type*")
        self.assertEquals(form.fields["peer_reviewed"].label, "Peer Reviewed*")
        self.assertEquals(form.fields["keywords"].label, "Keywords*")
        self.assertEquals(form.fields["website"].label, "Website")

        for visible in form.visible_fields():
            self.assertEquals(visible.field.widget.attrs["class"], "form-control")
            self.assertEquals(visible.field.widget.attrs.update({"style": "width:25em"}))

    def test_clean_name(self):
        form = VenueForm()
        if form.is_valid():
            form.clean_name()
            self.assertTrue(form.fields['name'].label is None or form.fields['name'].label == 'name')

    def test_clean_publisher(self):
        form = VenueForm()
        if form.is_valid():
            form.clean_publisher()
            self.assertTrue(form.fields['publisher'].label is None or form.fields['publisher'].label == 'publisher')

    def test_clean_publication_date(self):
        form = VenueForm()
        if form.is_valid():
            form.clean_publication_date()
            self.assertTrue(form.fields['publication_date'].label is None or form.fields['publication_date'].label == 'publication_date')

    def test_clean_type(self):
        form = VenueForm()
        if form.is_valid():
            form.clean_type()
            self.assertTrue(form.fields['type'].label is None or form.fields['type'].label == 'type')

    def test_clean_peer_reviewed(self):
        form = VenueForm()
        if form.is_valid():
            form.clean_peer_reviewed()
            self.assertTrue(form.fields['peer_reviewed'].label is None or form.fields['peer_reviewed'].label == 'peer_reviewed')

    def test_clean_keywords(self):
        form = VenueForm()
        if form.is_valid():
            form.clean_keywords()
            self.assertTrue(form.fields['keywords'].label is None or form.fields['keywords'].label == 'keywords')

    def test_clean_website(self):
        form = VenueForm()
        if form.is_valid():
            form.clean_website()
            self.assertTrue(form.fields['website'].label is None or form.fields['website'].label == 'website')

class CommentFormTest(TestCase):

    def test_fields(self):
        form = CommentForm()
        self.assertEquals(form.fields["text"].label, "")

        for visible in form.visible_fields():
            self.assertEquals(visible.field.widget.attrs["class"], "form-control")
            self.assertEquals(visible.field.widget.attrs.update({"style": "width:35em"}))

    def test_clean_text(self):
        form = CommentForm()
        if form.is_valid():
            form.clean_text()
            self.assertTrue(form.fields['text'].label is None or form.fields['text'].label == 'text')

    def test_clean_publication_date(self):
        form = CommentForm()
        if form.is_valid():
            form.clean_publication_date()
            self.assertTrue(form.fields['publication_date'].label is None or form.fields['publication_date'].label == 'publication_date')

class CodeFormTest(TestCase):

    def test_fields(self):
        form = CodeForm()
        self.assertEquals(form.fields["website"].label, "Website*")
        self.assertEquals(form.fields["keywords"].label, "Keywords*")
        self.assertEquals(form.fields["descriptions"].label, "Description*")

        for visible in form.visible_fields():
            self.assertEquals(visible.field.widget.attrs["class"], "form-control")
            self.assertEquals(visible.field.widget.attrs.update({"style": "width:25em"}))

    def test_clean_keywords(self):
        form = CodeForm()
        if form.is_valid():
            form.clean_keywords()
            self.assertTrue(form.fields['keywords'].label is None or form.fields['keywords'].label == 'keywords')

    def test_clean_description(self):
        form = CodeForm()
        if form.is_valid():
            form.clean_description()
            self.assertTrue(form.fields['description'].label is None or form.fields['description'].label == 'description')

    def test_clean_website(self):
        form = CodeForm()
        if form.is_valid():
            form.clean_website()
            self.assertTrue(form.fields['website'].label is None or form.fields['website'].label == 'website')





