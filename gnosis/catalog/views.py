from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from .models import Paper, Person, Dataset, Venue, Comment
from .forms import PaperForm, PersonForm, DatasetForm, VenueForm, CommentForm, SearchVenuesForm, SearchPapersForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from neomodel import db
from datetime import date
from nltk.corpus import stopwords


#
# Paper Views
#
def papers(request):
    return render(request, 'papers.html', {'papers': Paper.nodes.all(), 'num_papers': len(Paper.nodes.all())})


def paper_detail(request, id):
    # Retrieve the paper from the database
    query = "MATCH (a) WHERE ID(a)={id} RETURN a"
    results, meta = db.cypher_query(query, dict(id=id))
    if len(results) > 0:
        all_papers = [Paper.inflate(row[0]) for row in results]
        paper = all_papers[0]
    else:  # go back to the paper index page
        return render(request, 'papers.html', {'papers': Paper.nodes.all(), 'num_papers': len(Paper.nodes.all())})

    # Retrieve all comments about this paper.
    query = "MATCH (:Paper {title: {paper_title}})<--(c:Comment) RETURN c"
    results, meta = db.cypher_query(query, dict(paper_title=paper.title))
    if len(results) > 0:
        comments = [Comment.inflate(row[0]) for row in results]
        num_comments = len(comments)
    else:
        comments = []
        num_comments = 0

    # Retrieve venue where paper was published.
    query = "MATCH (:Paper {title: {paper_title}})-->(v:Venue) RETURN v"
    results, meta = db.cypher_query(query, dict(paper_title=paper.title))
    if len(results) > 0:
        venues = [Venue.inflate(row[0]) for row in results]
        venue = venues[0]
    else:
        venue = None

    request.session['last-viewed-paper'] = id
    return render(request,
                  'paper_detail.html',
                  {'paper': paper, 'venue': venue, 'comments': comments, 'num_comments': num_comments})


def paper_find(request):
    message = None
    if request.method == 'POST':
        form = SearchPapersForm(request.POST)
        print("Received POST request")
        if form.is_valid():
            english_stopwords = stopwords.words('english')
            paper_title = form.cleaned_data['paper_title'].lower()
            paper_title_tokens = [w for w in paper_title.split(' ') if not w in english_stopwords]
            paper_query = '(?i).*' + '+.*'.join('(' + w + ')' for w in paper_title_tokens) + '+.*'
            query = "MATCH (p:Paper) WHERE  p.title =~ { paper_query } RETURN p LIMIT 25"
            print("Cypher query string {}".format(query))
            results, meta = db.cypher_query(query, dict( paper_query=paper_query))
            if len(results) > 0:
                print("Found {} matching papers".format(len(results)))
                papers = [Paper.inflate(row[0]) for row in results]
                return render(request, 'paper_results.html', {'papers': papers})
            else:
                message = "No results found. Please try again!"

    elif request.method == 'GET':
        print("Received GET request")
        form = SearchPapersForm()

    return render(request, 'paper_find.html', {'form': form, 'message': message})


@login_required
def paper_connect_venue(request, id):

    if request.method == 'POST':
        form = SearchVenuesForm(request.POST)
        if form.is_valid():
            # search the db for the venue
            # if venue found, then link with paper and go back to paper view
            # if not, ask the user to create a new venue
            english_stopwords = stopwords.words('english')
            venue_name = form.cleaned_data['venue_name'].lower()
            venue_publication_year = form.cleaned_data['venue_publication_year']
            # TO DO: should probably check that data is 4 digits...
            venue_name_tokens = [w for w in venue_name.split(' ') if not w in english_stopwords]
            venue_query = '(?i).*' + '+.*'.join('(' + w + ')' for w in venue_name_tokens) + '+.*'
            query = "MATCH (v:Venue) WHERE v.publication_date =~ '" + venue_publication_year[0:4] + \
                    ".*' AND v.name =~ { venue_query } RETURN v"
            results, meta = db.cypher_query(query, dict(venue_publication_year=venue_publication_year[0:4],
                                                        venue_query=venue_query))
            if len(results) > 0:
                venues = [Venue.inflate(row[0]) for row in results]
                print("Found {} venues that match".format(len(venues)))
                for v in venues:
                    print("\t{}".format(v))

                if len(results) > 1:
                    # ask the user to select one of them
                    return render(request, 'paper_connect_venue.html', {'form': form,
                                                                        'venues': venues,
                                                                        'message': 'Found more than one matching venues. Please narrow your search'})
                else:
                    venue = venues[0]
                    print('Selected Venue: {}'.format(venue))

                # retrieve the paper
                query = "MATCH (a) WHERE ID(a)={id} RETURN a"
                results, meta = db.cypher_query(query, dict(id=id))
                if len(results) > 0:
                    all_papers = [Paper.inflate(row[0]) for row in results]
                    paper = all_papers[0]
                    print("Found paper: {}".format(paper.title))
                    # check if the paper is connect with a venue; if yes, the remove link to
                    # venue before adding link to the new venue
                    query = 'MATCH (p:Paper)-[r:was_published_at]->(v:Venue) where id(p)={id} return v'
                    results, meta = db.cypher_query(query, dict(id=id))
                    if len(results) > 0:
                        venues = [Venue.inflate(row[0]) for row in results]
                        for v in venues:
                            print("Disconnecting from: {}".format(v))
                            paper.was_published_at.disconnect(v)
                            paper.save()
                else:
                    print("Could not find paper!")
                    # should not get here since we started from the actual paper...but what if we do end up here?
                    pass  # Should raise an exception but for now just pass
                # we have a venue and a paper, so connect them.
                paper.was_published_at.connect(venue)
                paper.save()
                return render(request, 'papers.html',
                              {'papers': Paper.nodes.all(), 'num_papers': len(Paper.nodes.all())})

            else:
                # render new Venue form with the searched name as
                message = 'No matching venues found'

    if request.method == 'GET':
        form = SearchVenuesForm()
        message = None

    return render(request, 'paper_connect_venue.html', {'form': form, 'venues': None, 'message': message})


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
            paper_inst.keywords = form.cleaned_data['keywords']
            paper_inst.download_link = form.cleaned_data['download_link']
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
        form = PaperForm(initial={'title': paper_inst.title,
                                  'abstract': paper_inst.abstract,
                                  'keywords': paper_inst.keywords,
                                  'download_link': paper_inst.download_link, })

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

    # Retrieve the paper from the database
    query = "MATCH (a) WHERE ID(a)={id} RETURN a"
    results, meta = db.cypher_query(query, dict(id=id))
    if len(results) > 0:
        # There should be only one results because ID should be unique. Here we check that at
        # least one result has been returned and take the first result as the correct match.
        # Now, it should not happen that len(results) > 1 since IDs are meant to be unique.
        # For the MVP we are going to ignore the latter case and just continue but ultimately,
        # we should be checking for > 1 and failing gracefully.
        all_people = [Person.inflate(row[0]) for row in results]
        person = all_people[0]
    else:  # go back to the paper index page
        return render(request, 'people.html', {'people': Person.nodes.all(), 'num_people': len(Person.nodes.all())})

    #
    # TO DO: Retrieve all papers co-authored by this person and list them; same for
    # co-authors and advisees.
    #
    request.session['last-viewed-person'] = id
    return render(request,
                  'person_detail.html',
                  {'person': person})


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

    # Retrieve paper using paper id
    paper_id = request.session['last-viewed-paper']
    query = "MATCH (a) WHERE ID(a)={id} RETURN a"
    results, meta = db.cypher_query(query, dict(id=paper_id))
    if len(results) > 0:
        all_papers = [Paper.inflate(row[0]) for row in results]
        paper = all_papers[0]
    else:  # just send him to the list of papers
        HttpResponseRedirect(reverse('papers_index'))

    if request.method == 'POST':
        comment = Comment()
        comment.created_by = user.id
        comment.author = user.username
        form = CommentForm(instance=comment, data=request.POST)
        if form.is_valid():
            # add link from new comment to paper
            form.save()
            comment.discusses.connect(paper)
            del request.session['last-viewed-paper']
            return redirect('paper_detail', id=paper_id)
            #return render(request, 'paper_detail.html', {'paper': paper})
            # return HttpResponseRedirect(reverse('comments_index'))
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


