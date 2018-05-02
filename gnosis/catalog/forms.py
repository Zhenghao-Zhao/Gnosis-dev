from django.forms import ModelForm
from .models import Paper, Person, Dataset


class PaperForm(ModelForm):

    def clean_title(self):
        return self.cleaned_data['title']

    def clean_abstract(self):
        return self.cleaned_data['abstract']

    def clean_keywords(self):
        return self.cleaned_data['keywords']

    class Meta:
        model = Paper
        fields = ['title', 'abstract', 'keywords']


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
