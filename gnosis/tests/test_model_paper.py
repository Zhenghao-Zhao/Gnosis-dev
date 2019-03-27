from django.test import TestCase

from catalog.models import Paper
from neomodel.exceptions import RequiredProperty


# Create your tests here.
class PaperModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self) -> None:
        pass

    def test_object_create(self):

        paper = Paper()
        paper.title = "No title"
        paper.abstract = "The abstract is missing."
        paper.keywords = ""
        paper.download_link = "https://google.com"

        self.assertEquals(paper.title, "No title")
        self.assertEquals(paper.__str__(), "No title")
        self.assertEquals(paper.abstract, "The abstract is missing.")
        self.assertEquals(paper.download_link, "https://google.com")
        self.assertEquals(len(paper.keywords), 0)

        paper = Paper()
        paper.abstract = "The abstract is missing."
        paper.keywords = ""
        paper.download_link = "https://google.com"

        try:  # It is missing required property title
            paper.save()
        except RequiredProperty:
            assert True
        else:
            assert False

        paper = Paper()
        paper.title = "No title"
        paper.keywords = ""
        paper.download_link = "https://google.com"

        try:  # It is missing required property abstract
            paper.save()
        except RequiredProperty:
            assert True
        else:
            assert False

        paper = Paper()
        paper.title = "No title"
        paper.abstract = ""
        paper.keywords = ""

        try:  # It is missing required property download_link
            paper.save()
        except RequiredProperty:
            assert True
        else:
            assert False

    def test_create_delete_in_db(self):
        """ For this test, a neo4j database must be running """
        paper = Paper(title="No title",
                      abstract="The abstract is missing.",
                      keywords="test, paper",
                      download_link="https://google.com"
                      )

        self.assertTrue(paper)

        # This will create an entry in the db.
        paper.save()

        # How can I check that the paper was added to the db?
        papers = Paper.nodes.filter(title="No title")

        self.assertEquals(len(papers), 1)
        # delete the paper from the DB
        papers[0].delete()

        # check if the paper was indeed deleted
        papers = Paper.nodes.filter(title="No title")
        self.assertEquals(len(papers), 0)
