from django.test import TestCase
from django.contrib.auth.models import User
from catalog.views.views import(
    _find_paper,
    paper_create_from_url,
)
from neomodel.exceptions import RequiredProperty
from django.http import HttpRequest


# Create your tests here.
class PaperImport(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='luke', email='luke@luke.com', password='luke123')

    def test_url_paper_valid_import(self):
        """ For this test, a neo4j database must be running """
        request = HttpRequest()
        request.user = self.user
        request.method = 'POST'
        request.session = {}

        # test for arxiv url
        request.POST["url"] = "https://arxiv.org/abs/1607.00653"
        paper_create_from_url(request)

        # test specific entries
        self.assertEquals(request.session["from_external"], True)
        self.assertEquals(request.session["external_title"], "node2vec: Scalable Feature Learning for Networks")
        self.assertEquals(request.session["external_abstract"][1:11], "Prediction")
        self.assertEquals(request.session["external_abstract"][-10:], "networks.\n")
        self.assertEquals(request.session["external_url"], "https://arxiv.org/abs/1607.00653")
        self.assertEquals(request.session["external_authors"], "Aditya Grover, Jure Leskovec\n")

        # test for NeurIPS url
        request.POST["url"] = "papers.nips.cc/paper/7286-efficient-algorithms-for-" \
                              "non-convex-isotonic-regression-through-submodular-optimization"

        paper_create_from_url(request)

        # test specific entries
        self.assertEquals(request.session["from_external"], True)
        self.assertEquals(request.session["external_title"],
                          "Efficient Algorithms for Non-convex Isotonic Regression through Submodular Optimization")
        self.assertEquals(request.session["external_abstract"][:2], "We")
        self.assertEquals(request.session["external_abstract"][-5:], "time.")
        self.assertEquals(request.session["external_url"],
                          "https://papers.nips.cc/paper/7286-efficient-algorithms-for-non-convex"
                          "-isotonic-regression-through-submodular-optimization")
        self.assertEquals(request.session["external_authors"], "Francis Bach")



    # def test_url_paper_invalid_import(self):
    #     request = HttpRequest()
    #     request.user = self.user
    #     request.method = 'POST'
    #     request.POST["url"] = "https://arxiv.org/abs/1607"
    #     request.session = {}
    #     paper_create_from_url(request)
    #     result = _find_paper("node2vec")
    #     self.assertEquals(len(result), 1)
    #     print(result[0])
