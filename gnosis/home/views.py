from django.shortcuts import render
from catalog.models import Paper, Person


# Create your views here.
def home(request):
    num_papers = len(Paper.nodes.all())
    num_people = len(Person.nodes.all())

    return render(request, 'home.html', {'num_papers': num_papers, 'num_people': num_people})
