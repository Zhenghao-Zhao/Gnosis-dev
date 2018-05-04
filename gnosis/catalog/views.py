from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import Paper, Person, Dataset, Venue, Comment
from .forms import PaperForm, PersonForm, DatasetForm, VenueForm, CommentForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from neomodel import db
from datetime import date


#
# Paper Views
#
def papers(request):
    return render(request, 'papers.html', {'papers': Paper.nodes.all(), 'num_papers': len(Paper.nodes.all())})


def paper_detail(request, id):
    return render(request, 'paper_detail.html', {'paper': Paper.nodes.all()})


@login_required
def paper_update(request, id):
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

@login_required
def paper_create(request):
    user = request.user

    if request.method == 'POST':
        paper = Paper()
        paper.created_by = user.id
        form = PaperForm(instance=paper, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('papers_index'))
    else:  # GET
        form = PaperForm()

    return render(request, 'paper_form.html', {'form': form})


#
# Person Views
#
def persons(request):
    return render(request, 'people.html', {'people': Person.nodes.all(), 'num_people': len(Person.nodes.all())})


def person_detail(request, id):
    return render(request, 'person_detail.html', {'person': Person.nodes.all()})


@login_required
def person_create(request):
    user = request.user

    if request.method == 'POST':
        person = Person()
        person.created_by = user.id
        form = PersonForm(instance=person, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('persons_index'))
    else:  # GET
        form = PersonForm()

    return render(request, 'person_form.html', {'form': form})

@login_required
def person_update(request, id):
    # retrieve paper by ID
    # https://github.com/neo4j-contrib/neomodel/issues/199
    query = "MATCH (a) WHERE ID(a)={id} RETURN a"
    results, meta = db.cypher_query(query, dict(id=id))
    if len(results) > 0:
        all_people = [Person.inflate(row[0]) for row in results]
        person_inst = all_people[0]
    else:
        person_inst = Person()

    # if this is POST request then process the Form data
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            person_inst.first_name = form.cleaned_data['first_name']
            person_inst.middle_name = form.cleaned_data['middle_name']
            person_inst.last_name = form.cleaned_data['last_name']
            person_inst.affiliation = form.cleaned_data['affiliation']
            person_inst.website = form.cleaned_data['website']
            person_inst.save()

            return HttpResponseRedirect(reverse('persons_index'))
    # GET request
    else:
        query = "MATCH (a) WHERE ID(a)={id} RETURN a"
        results, meta = db.cypher_query(query, dict(id=id))
        if len(results) > 0:
            all_people = [Person.inflate(row[0]) for row in results]
            person_inst = all_people[0]
        else:
            person_inst = Person()
        form = PersonForm(initial={'first_name': person_inst.first_name,
                                   'middle_name': person_inst.middle_name,
                                   'last_name': person_inst.last_name,
                                   'affiliation': person_inst.affiliation,
                                   'website': person_inst.website,
                                   }
                          )

    return render(request, 'person_update.html', {'form': form, 'person': person_inst})

#
# Dataset Views
#
def datasets(request):
    return render(request, 'datasets.html', {'datasets': Dataset.nodes.all(), 'num_datasets': len(Dataset.nodes.all())})


def dataset_detail(request, id):
    return render(request, 'dataset_detail.html', {'dataset': Dataset.nodes.all()})


@login_required
def dataset_create(request):
    user = request.user

    if request.method == 'POST':
        dataset = Dataset()
        dataset.created_by = user.id
        form = DatasetForm(instance=dataset, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('datasets_index'))
    else:  # GET
        form = DatasetForm()

    return render(request, 'dataset_form.html', {'form': form})

@login_required
def dataset_update(request, id):
    # retrieve paper by ID
    # https://github.com/neo4j-contrib/neomodel/issues/199
    query = "MATCH (a) WHERE ID(a)={id} RETURN a"
    results, meta = db.cypher_query(query, dict(id=id))
    if len(results) > 0:
        datasets = [Dataset.inflate(row[0]) for row in results]
        dataset = datasets[0]
    else:
        dataset = Dataset()

    # if this is POST request then process the Form data
    if request.method == 'POST':
        form = DatasetForm(request.POST)
        if form.is_valid():
            dataset.name = form.cleaned_data['name']
            dataset.source_type = form.cleaned_data['source_type']
            dataset.website = form.cleaned_data['website']
            dataset.save()

            return HttpResponseRedirect(reverse('datasets_index'))
    # GET request
    else:
        query = "MATCH (a) WHERE ID(a)={id} RETURN a"
        results, meta = db.cypher_query(query, dict(id=id))
        if len(results) > 0:
            datasets = [Dataset.inflate(row[0]) for row in results]
            dataset = datasets[0]
        else:
            dataset = Dataset()
        form = DatasetForm(initial={'name': dataset.name,
                                    'source_type': dataset.source_type,
                                    'website': dataset.website,
                                    }
                           )

    return render(request, 'dataset_update.html', {'form': form, 'dataset': dataset})


#
# Venue Views
#
def venues(request):
    return render(request, 'venues.html', {'venues': Venue.nodes.all(), 'num_venues': len(Venue.nodes.all())})


def venue_detail(request, id):
    return render(request, 'venue_detail.html', {'venue': Venue.nodes.all()})


@login_required
def venue_create(request):
    user = request.user

    if request.method == 'POST':
        venue = Venue()
        venue.created_by = user.id
        form = VenueForm(instance=venue, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('venues_index'))
    else:  # GET
        form = VenueForm()

    return render(request, 'venue_form.html', {'form': form})

@login_required
def venue_update(request, id):
    # retrieve paper by ID
    # https://github.com/neo4j-contrib/neomodel/issues/199
    query = "MATCH (a) WHERE ID(a)={id} RETURN a"
    results, meta = db.cypher_query(query, dict(id=id))
    if len(results) > 0:
        venues = [Venue.inflate(row[0]) for row in results]
        venue = venues[0]
    else:
        venue = Venue()

    # if this is POST request then process the Form data
    if request.method == 'POST':
        form = VenueForm(request.POST)
        if form.is_valid():
            venue.name = form.cleaned_data['name']
            venue.publication_date = form.cleaned_data['publication_date']
            venue.type = form.cleaned_data['type']
            venue.publisher = form.cleaned_data['publisher']
            venue.keywords = form.cleaned_data['keywords']
            venue.peer_reviewed = form.cleaned_data['peer_reviewed']
            venue.website = form.cleaned_data['website']
            venue.save()

            return HttpResponseRedirect(reverse('venues_index'))
    # GET request
    else:
        query = "MATCH (a) WHERE ID(a)={id} RETURN a"
        results, meta = db.cypher_query(query, dict(id=id))
        if len(results) > 0:
            venues = [Venue.inflate(row[0]) for row in results]
            venue = venues[0]
        else:
            venue = Venue()
        form = VenueForm(initial={'name': venue.name,
                                  'type': venue.type,
                                  'publication_date': venue.publication_date,
                                  'publisher': venue.publisher,
                                  'keywords': venue.keywords,
                                  'peer_reviewed': venue.peer_reviewed,
                                  'website': venue.website,
                                  }
                         )

    return render(request, 'venue_update.html', {'form': form, 'venue': venue})


#
# Comment Views
#
def comments(request):
    return render(request, 'comments.html', {'comments': Comment.nodes.all(), 'num_comments': len(Comment.nodes.all())})


def comment_detail(request, id):
    return render(request, 'comment_detail.html', {'comment': Comment.nodes.all()})


@login_required
def comment_create(request):
    user = request.user

    if request.method == 'POST':
        comment = Comment()
        comment.created_by = user.id
        comment.author = user.username
        form = CommentForm(instance=comment, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('comments_index'))
    else:  # GET
        form = CommentForm()

    return render(request, 'comment_form.html', {'form': form})

@login_required
def comment_update(request, id):
    # retrieve paper by ID
    # https://github.com/neo4j-contrib/neomodel/issues/199
    query = "MATCH (a) WHERE ID(a)={id} RETURN a"
    results, meta = db.cypher_query(query, dict(id=id))
    if len(results) > 0:
        comments = [Comment.inflate(row[0]) for row in results]
        comment = comments[0]
    else:
        comment = Comment()

    # if this is POST request then process the Form data
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment.text = form.cleaned_data['text']
            # comment.author = form.cleaned_data['author']
            comment.save()

            return HttpResponseRedirect(reverse('comments_index'))
    # GET request
    else:
        query = "MATCH (a) WHERE ID(a)={id} RETURN a"
        results, meta = db.cypher_query(query, dict(id=id))
        if len(results) > 0:
            comments = [Comment.inflate(row[0]) for row in results]
            comment = comments[0]
        else:
            comment = Comment()
        # form = CommentForm(initial={'author': comment.author,
        #                             'text': comment.text,
        #                             'publication_date': comment.publication_date,
        #                             }
        #                    )
        form = CommentForm(initial={'text': comment.text,
                                    'publication_date': comment.publication_date,
                                    }
                           )


    return render(request, 'comment_update.html', {'form': form, 'comment': comment})


#
# Utility Views (admin required)
#
@login_required
def build(request):

    try:
        d1 = Dataset()
        d1.name = 'Yelp'
        d1.source_type = 'N'
        d1.save()

        v1 = Venue()
        v1.name = 'Neural Information Processing Systems'
        v1.publication_date = date(2017, 12, 15)
        v1.type = 'C'
        v1.publisher = 'NIPS Foundation'
        v1.keywords = 'machine learning, machine learning, computational neuroscience'
        v1.website = 'https://nips.cc'
        v1.peer_reviewed = 'Y'
        v1.save()

        v2 = Venue()
        v2.name = 'International Conference on Machine Learning'
        v2.publication_date = date(2016, 5, 24)
        v2.type = 'C'
        v2.publisher = 'International Machine Learning Society (IMLS)'
        v2.keywords = 'machine learning, computer science'
        v2.peer_reviewed = 'Y'
        v2.website = 'https://icml.cc/2016/'
        v2.save()


        p1 = Paper()
        p1.title = 'The best paper in the world.'
        p1.abstract = 'Abstract goes here'
        p1.keywords = 'computer science, machine learning, graphs'
        p1.save()

        p1.evaluates_on.connect(d1)
        p1.was_published_at.connect(v1)

        p2 = Paper()
        p2.title = 'The second best paper in the world.'
        p2.abstract = 'Abstract goes here'
        p2.keywords = 'statistics, robust methods'
        p2.save()

        p2.cites.connect(p1)
        p2.was_published_at.connect(v2)

        p3 = Paper()
        p3.title = 'I wish I could write a paper with a great title.'
        p3.abstract = 'Abstract goes here'
        p3.keywords = 'machine learning, neural networks, convolutional neural networks'
        p3.save()

        p3.cites.connect(p1)
        p3.was_published_at.connect(v1)

        a1 = Person()
        a1.first_name = 'Pantelis'
        a1.last_name = 'Elinas'
        a1.save()

        a1.authors.connect(p1)

        a2 = Person()
        a2.first_name = "Ke"
        a2.last_name = "Sun"
        a2.save()

        a2.authors.connect(p1)
        a2.authors.connect(p2)

        a3 = Person()
        a3.first_name = "Bill"
        a3.last_name = "Gates"
        a3.save()

        a3.authors.connect(p3)
        a3.advisor_of.connect(a1)

        a4 = Person()
        a4.first_name = "Steve"
        a4.last_name = "Jobs"
        a4.save()

        a4.authors.connect(p2)
        a4.authors.connect(p3)

        a4.co_authors_with.connect(a3)

        c1 = Comment()
        c1.author = "Pantelis Elinas"
        c1.text = "This paper is flawless"
        c1.save()

        c1.discusses.connect(p1)

    except Exception:
        pass

    num_papers = len(Paper.nodes.all())
    num_people = len(Person.nodes.all())

    return render(request, 'build.html', {'num_papers': num_papers, 'num_people': num_people})


