from django.db import models
from datetime import datetime
from django_neomodel import DjangoNode
from django.urls import reverse
from neomodel import StructuredNode, StringProperty, DateTimeProperty, UniqueIdProperty, IntegerProperty, \
    Relationship, RelationshipTo


# Create your models here.
class Paper(DjangoNode):

    uid = UniqueIdProperty()
    title = StringProperty(required=True)
    abstract = StringProperty(required=True)
    published_year = DateTimeProperty(default=datetime.now())

    created = DateTimeProperty(default=datetime.now())
    created_by = IntegerProperty()  # The uid of the user who created this node

    cites = RelationshipTo("Paper", "CITES")

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


class Author(DjangoNode):

    uid = UniqueIdProperty()
    first_name = StringProperty()
    last_name = StringProperty()
    affiliation = StringProperty()

    is_author = RelationshipTo("Paper", "IS_AUTHOR")

    created = DateTimeProperty(default=datetime.now())

    class Meta:
        app_label = 'catalog'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return '{%s}. {%s}'.format(self.first_name[0], self.last_name)

    def get_absolute_url(self):
        return reverse('author-detail', args=[self.id])