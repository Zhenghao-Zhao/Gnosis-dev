from django.db import models
from datetime import datetime
from django_neomodel import DjangoNode
from django.urls import reverse
from neomodel import StructuredNode, StringProperty, DateTimeProperty, DateProperty, UniqueIdProperty, \
    IntegerProperty, Relationship, RelationshipTo


# Create your models here.
class Paper(DjangoNode):

    uid = UniqueIdProperty()

    created = DateTimeProperty(default=datetime.now())
    created_by = IntegerProperty()  # The uid of the user who created this node

    # These are always required
    title = StringProperty(required=True)
    abstract = StringProperty(required=True)
    keywords = StringProperty(required=True)

    # Links
    cites = RelationshipTo("Paper", "cites")
    uses = RelationshipTo("Paper", "uses")
    extends = RelationshipTo("Paper", "extends")
    evaluates_on = RelationshipTo("Dataset", "evaluates_on")
    was_published_at = RelationshipTo("Venue", "was_published_at")
    published = RelationshipTo("Dataset", "published")

    class Meta:
        app_label = 'catalog'
        ordering = ["title", "-published"]  # title is A-Z and published is from newest to oldest

    def __str__(self):
        """
        String for representing the Paper object, e.g., in Admin site.
        :return: The paper's title
        """
        return self.title

    def get_absolute_url(self):
        return reverse('paper_detail', args=[self.id])


class Person(DjangoNode):

    uid = UniqueIdProperty()
    created = DateTimeProperty(default=datetime.now())
    created_by = IntegerProperty()  # The uid of the user who created this node

    # These are always required
    first_name = StringProperty(required=True)
    last_name = StringProperty(required=True)
    middle_name = StringProperty()
    affiliation = StringProperty()
    website = StringProperty()

    authors = RelationshipTo("Paper", "authors")
    co_authors_with = RelationshipTo("Person", "co_authors_with")
    advisor_of = RelationshipTo("Person", "advisor_of")

    class Meta:
        app_label = 'catalog'
        ordering = ['last_name', 'first_name', 'affiliation']

    def __str__(self):
        return '{%s} {%s} {%s}'.format(self.first_name[0], self.middle_name, self.last_name)

    def get_absolute_url(self):
        return reverse('person-detail', args=[self.id])


class Dataset(DjangoNode):

    uid = UniqueIdProperty()
    created = DateTimeProperty(default=datetime.now())
    created_by = IntegerProperty()  # The uid of the user who created this node

    # These are always required
    name = StringProperty(required=True)
    type = StringProperty(required=True)

    website = StringProperty()

    class Meta:
        app_label = 'catalog'
        ordering = ['last_name', 'first_name', 'affiliation']

    def __str__(self):
        return '{%s}'.format(self.name)

    def get_absolute_url(self):
        return reverse('dataset-detail', args=[self.id])


class Venue(DjangoNode):

    uid = UniqueIdProperty()
    created = DateTimeProperty(default=datetime.now())
    created_by = IntegerProperty()  # The uid of the user who created this node

    # These are always required
    name = StringProperty(required=True)
    publication_date = DateProperty(required=True)
    type = StringProperty(required=True)  # journal, tech report, open source, conference, workshop
    publisher = StringProperty(required=True)
    keywords = StringProperty(required=True)

    peer_reviewed = StringProperty(choices=(('Yes', 'Y'), ('No', 'N')), default='No')  # Yes or no
    website = StringProperty()

    class Meta:
        app_label = 'catalog'
        ordering = ['name', 'publication_date']

    def __str__(self):
        return '{%s}'.format(self.name)

    def get_absolute_url(self):
        return reverse('venue-detail', args=[self.id])


class Comment(DjangoNode):

    uid = UniqueIdProperty()
    created = DateTimeProperty(default=datetime.now())
    created_by = IntegerProperty()  # The uid of the user who created this node

    # These are always required
    author = StringProperty(required=True)  # required but should be able to get it from user object
    text = StringProperty(required=True)

    publication_date = DateTimeProperty(default_now=True)

    discusses = RelationshipTo("Paper", "discusses")

    class Meta:
        app_label = 'catalog'
        ordering = ['publication_date']

    def __str__(self):
        return '{%s}'.format(self.author)

    def get_absolute_url(self):
        return reverse('comment-detail', args=[self.id])
