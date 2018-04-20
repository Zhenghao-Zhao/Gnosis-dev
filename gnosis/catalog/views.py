from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import Paper, Author
from .forms import PaperForm, AuthorForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from neomodel import db

def papers(request):
    return render(request, 'papers.html', {'papers': Paper.nodes.all(), 'num_papers': len(Paper.nodes.all())})


def paper_detail(request, id):
    return render(request, 'paper_detail.html', {'paper': Paper.nodes.all()})


@login_required
def paper_update(request, id):
    #paper_inst = Paper.nodes.all()[0]  # jsut take the first node; should find the one with id
    #paper_inst = Paper.nodes.filter(id = id)
    # retrieve paper by ID
    # https://github.com/neo4j-contrib/neomodel/issues/199
    query = "MATCH (a) WHERE ID(a)={id} RETURN a"
    results, meta = db.cypher_query(query, dict(id=id))
    if len(results) > 0:
        all_papers = [Paper.inflate(row[0]) for row in results]
        paper_inst = all_papers[0]
    else:
        paper_inst = Paper()

    # if this is POST request then process the Form data
    if request.method == 'POST':

        form = PaperForm(request.POST)
        if form.is_valid():
            paper_inst.title = form.cleaned_data['title']
            paper_inst.abstract = form.cleaned_data['abstract']
            paper_inst.save()

            return HttpResponseRedirect(reverse('papers_index'))
    # GET request
    else:
        query = "MATCH (a) WHERE ID(a)={id} RETURN a"
        results, meta = db.cypher_query(query, dict(id=id))
        if len(results) > 0:
            all_papers = [Paper.inflate(row[0]) for row in results]
            paper_inst = all_papers[0]
        else:
            paper_inst = Paper()
        # paper_inst = Paper()
        form = PaperForm(initial={'title': paper_inst.title, 'abstract': paper_inst.abstract, })

    return render(request, 'paper_update.html', {'form': form, 'paper': paper_inst})


def authors(request):
    return render(request, 'authors.html', {'authors': Author.nodes.all(), 'num_authors': len(Author.nodes.all())})


def author_create(request):
    author = Author()

    form = AuthorForm()

    return render(request, 'author_form.html', {'form': form, 'author': author})


@login_required
def build(request):

    try:
        p1 = Paper()
        p1.title = "The best paper in the world."
        p1.save()

        p2 = Paper()
        p2.title = "The second best paper in the world."
        p2.save()

        p2.cites.connect(p1)

        p3 = Paper()
        p3.title = "I wish I could write a paper with a great title."
        p3.save()

        p3.cites.connect(p1)

        a1 = Author()
        a1.first_name = 'Pantelis'
        a1.last_name = 'Elinas'
        a1.save()

        a1.is_author.connect(p1)

        a2 = Author()
        a2.first_name = "Ke"
        a2.last_name = "Sun"
        a2.save()

        a2.is_author.connect(p1)
        a2.is_author.connect(p2)

        a3 = Author()
        a3.first_name = "Bill"
        a3.last_name = "Gates"
        a3.save()

        a3.is_author.connect(p3)

        a4 = Author()
        a4.first_name = "Steve"
        a4.last_name = "Jobs"
        a4.save()

        a4.is_author.connect(p2)
        a4.is_author.connect(p3)

    except Exception:
        pass

    num_papers = len(Paper.nodes.all())
    num_authors = len(Author.nodes.all())

    return render(request, 'build.html', {'num_papers': num_papers, 'num_authors': num_authors})


