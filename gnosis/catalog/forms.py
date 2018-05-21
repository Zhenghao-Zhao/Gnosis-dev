from django import forms
from django.forms import ModelForm, Form
from .models import Paper, Person, Dataset, Venue, Comment


#
# Search forms
#
class SearchVenuesForm(Form):

    def clean_venue_name(self):
        return self.cleaned_data['venue_name']

    def clean_venue_publication_year(self):
        return self.cleaned_data['venue_publication_year']

    venue_name = forms.CharField(required=True)
    venue_publication_year = forms.CharField(required=True)


#
# Model forms
#
class PaperForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_title(self):
        return self.cleaned_data['title']

    def clean_abstract(self):
        return self.cleaned_data['abstract']

    def clean_keywords(self):
        return self.cleaned_data['keywords']

    def clean_download_link(self):
        return self.cleaned_data['download_link']

    class Meta:
        model = Paper
        fields = ['title', 'abstract', 'keywords', 'download_link']


class PersonForm(ModelForm):

    def clean_first_name(self):
        return self.cleaned_data['first_name']

    def clean_middle_name(self):
        return self.cleaned_data['middle_name']

    def clean_last_name(self):
        return self.cleaned_data['last_name']

    def clean_affiliation(self):
        return self.cleaned_data['affiliation']

    def clean_website(self):
        return self.cleaned_data['website']

    class Meta:
        model = Person
        fields = ['first_name', 'middle_name', 'last_name', 'affiliation', 'website']


class DatasetForm(ModelForm):

    def clean_name(self):
        return self.cleaned_data['name']

    def clean_source_type(self):
        return self.cleaned_data['source_type']

    def clean_website(self):
        return self.cleaned_data['website']

    class Meta:
        model = Dataset
        fields = ['name', 'source_type', 'website']


class VenueForm(ModelForm):

    def clean_name(self):
        return self.cleaned_data['name']

    def clean_publisher(self):
        return self.cleaned_data['publisher']

    def clean_publication_date(self):
        return self.cleaned_data['publication_date']

    def clean_type(self):
        return self.cleaned_data['type']

    def clean_peer_reviewed(self):
        return self.cleaned_data['peer_reviewed']

    def clean_keywords(self):
        return self.cleaned_data['keywords']

    def clean_website(self):
        return self.cleaned_data['website']

    class Meta:
        model = Venue
        fields = ['name', 'publisher', 'publication_date', 'type', 'peer_reviewed', 'keywords', 'website']


class CommentForm(ModelForm):

    def clean_text(self):
        return self.cleaned_data['text']

    def clean_publication_date(self):
        return self.cleaned_data['publication_date']

    # def clean_author(self):
    #     return self.cleaned_data['author']

    class Meta:
        model = Comment
        fields = ['text']
