from django.shortcuts import render
from catalog.models import Paper, Person
from neomodel import db


# Create your views here.
def home(request):
    num_papers = len(Paper.nodes.all())
    num_people = len(Person.nodes.all())

    recent_papers = Paper.nodes.order_by('-created')[:5]
    authors = [', '.join(get_paper_authors(paper)) for paper in recent_papers]

    papers = list(zip(recent_papers, authors))

    return render(request, 'home.html', {'papers': papers,
                                         'num_papers': num_papers,
                                         'num_people': num_people})


def get_paper_authors(paper):
    query = "MATCH (:Paper {title: {paper_title}})<--(a:Person) RETURN a"
    results, meta = db.cypher_query(query, dict(paper_title=paper.title))
    if len(results) > 0:
        authors = [Person.inflate(row[0]) for row in results]
    else:
        authors = []
    # pdb.set_trace()
    authors = ['{}. {}'.format(author.first_name[0], author.last_name) for author in authors]

    return authors
