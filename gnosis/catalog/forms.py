from django.forms import ModelForm
from .models import Paper, Author


class PaperForm(ModelForm):

    def clean_title(self):
        return self.cleaned_data['title']

    def clean_abstract(self):
        return self.cleaned_data['abstract']

    class Meta:
        model = Paper
        fields = ['title', 'abstract']


class AuthorForm(ModelForm):

    def clean_first_name(self):
        return self.cleaned_data['first_name']

    def clean_last_name(self):
        return self.cleaned_data['last_name']

    def clean_affiliation(self):
        return self.cleaned_data['affiliation']


    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'affiliation', ]
