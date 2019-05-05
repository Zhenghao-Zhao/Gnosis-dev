from django.test import TestCase
from django.contrib.auth.models import User, Permission
from catalog.models import Paper
from catalog.views.views import get_paper_authors, paper_create
from django.http import HttpRequest


# Create your tests here.
# To run this test, use command: py -3 manage.py test tests.test_form_paper
class PaperViewTest(TestCase):
    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        self.user = User.objects.create_user(
            username='gnosis', email='gnosis@gnosis.com', password='gnosis')

        test_user1.save()
        test_user2.save()

    def test_paper_create(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')  # test views requires login
        request = HttpRequest()
        request.user = self.user
        request.method = 'POST'
        request.session = {}
        response = paper_create(request)
        self.assertEquals(response.status_code, 200)        # test if response is correct
        self.assertTrue("New Paper" in str(response.content) and "Title*" in str(response.content)
                        and "Abstract" in str(response.content) and "Keywords" in str(response.content))

