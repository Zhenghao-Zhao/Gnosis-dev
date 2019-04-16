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
            username='gnosis', email='gnosis@gnosis.com', password='gnosis')

    def test_import_content(self):
        """ For this test, a neo4j database must be running """
        request = HttpRequest()
        request.user = self.user
        request.method = 'POST'
        request.session = {}

        # test for arxiv url
        request.POST["url"] = "https://arxiv.org/abs/1607.00653"
        re = paper_create_from_url(request)
        self.assertTrue('location' in re._headers)      # check if it redirects to the paper create page

        # test whether specific entries are accurate
        self.assertEquals(request.session["from_external"], True)
        self.assertEquals(request.session["external_title"], "node2vec: Scalable Feature Learning for Networks")
        self.assertEquals(request.session["external_abstract"][1:11], "Prediction")
        self.assertEquals(request.session["external_abstract"][-10:], "networks.\n")
        self.assertEquals(request.session["external_url"], "https://arxiv.org/abs/1607.00653")
        self.assertEquals(request.session["external_authors"], "Aditya Grover, Jure Leskovec\n")

        # test for NeurIPS url
        request.POST["url"] = "papers.nips.cc/paper/7286-efficient-algorithms-for-" \
                              "non-convex-isotonic-regression-through-submodular-optimization"

        re = paper_create_from_url(request)
        self.assertTrue('location' in re._headers)     # check if it redirects to the paper create page

        # test whether specific entries are accurate
        self.assertEquals(request.session["from_external"], True)
        self.assertEquals(request.session["external_title"],
                          "Efficient Algorithms for Non-convex Isotonic Regression through Submodular Optimization")
        self.assertEquals(request.session["external_abstract"][:2], "We")
        self.assertEquals(request.session["external_abstract"][-5:], "time.")
        self.assertEquals(request.session["external_url"],
                          "https://papers.nips.cc/paper/7286-efficient-algorithms-for-non-convex"
                          "-isotonic-regression-through-submodular-optimization")
        self.assertEquals(request.session["external_authors"], "Francis Bach")

    def test_import_invalid_urls(self):
        request = HttpRequest()
        request.user = self.user
        request.method = 'POST'
        request.session = {}

        # test unsupported url
        url = "www.google.com"
        request.POST["url"] = url
        re = paper_create_from_url(request)
        # check that it does not redirect to the paper create page
        self.assertFalse('location' in re._headers)

        # test supported but invalid urls, i.e. content cannot be extracted
        invalid_urls = [
            "https://arxiv.org",                        # homepage of arxiv
            "https://arxiv.org/archive/astro-ph",     # topic selection page
            "https://arxiv.org/year/astro-ph/10",     # year selection page
            "https://arxiv.org/list/astro-ph/1001",   # selected results page(list of papers)
            # NeurIPS urls
            "https://papers.nips.cc/book/advances-in-neural-information-processing-systems-13-2000",  # all papers of 2010
            "https://papers.nips.cc/"                   # all papers
            ]
        for url in invalid_urls:
            request.POST["url"] = url
            re = paper_create_from_url(request)
            # check that it does not redirect to the paper create page
            self.assertFalse('location' in re._headers)


    def test_import_valid_urls(self):
        request = HttpRequest()
        request.user = self.user
        request.method = 'POST'
        request.session = {}
        valid_urls = [
            "https://arxiv.org/abs/1904.06351",         # paper from 2019
            "https://arxiv.org/abs/1904.06352",
            "https://arxiv.org/abs/astro-ph/9204001",  # paper from 1992
            "https://arxiv.org/abs/astro-ph/9301001",
            "https://arxiv.org/abs/astro-ph/0001001",  # paper from 2000
            "https://arxiv.org/abs/1001.0005",          # paper from 2010
            # NIPS papers
            "https://papers.nips.cc/paper/7292-doubly-robust-bayesian-inference-for-non-stationary"
            "-streaming-data-with-beta-divergences",   # paper from 2018
            "https://papers.nips.cc/paper/4123-"       # paper from 2010
            "repeated-games-against-budgeted-adversaries",
            "https://papers.nips.cc/paper/1799-who-"   # paper from 2000
            "does-what-a-novel-algorithm-to-determine-function-localization",
            ]
        for url in valid_urls:
            request.POST["url"] = url
            paper_create_from_url(request)
            self.assertEquals(request.session["from_external"], True)

