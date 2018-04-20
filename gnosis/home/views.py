from django.shortcuts import render
from catalog.models import Paper, Author

# Create your views here.
def home(request):
    num_papers = len(Paper.nodes.all())
    num_authors = len(Author.nodes.all())

    return render(request, 'home.html', {'num_papers': num_papers, 'num_authors': num_authors})
