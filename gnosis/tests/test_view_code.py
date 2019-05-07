from django.test import TestCase
from django.contrib.auth.models import User, Permission
from catalog.models import Code
from catalog.views.views import code_create, code_update, code_find, codes
from django.http import HttpRequest


# Create your tests here.
# To run this test, use command: py -3 manage.py test tests.test_form_paper
class CodeViewTest(TestCase):
    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        self.user = User.objects.create_user(
            username='gnosis', email='gnosis@gnosis.com', password='gnosis')

        test_user1.save()
        test_user2.save()

    def test_codes(self):
        request = HttpRequest()
        response = codes(request)
        self.assertEquals(response.status_code, 200)


    def test_code_create(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')  # test views requires login
        request = HttpRequest()
        request.user = self.user
        request.method = 'POST'
        request.session = {}
        response = code_create(request)
        self.assertEquals(response.status_code, 200)        # test if response is correct
        self.assertTrue("New Code" in str(response.content) and "Website*" in str(response.content)
                        and "Keywords*" in str(response.content) and "Description*" in str(response.content))

    def test_code_update(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')  # test views requires login
        request = HttpRequest()
        request.user = self.user
        request.method = 'POST'
        request.session = {}
        response = code_update(request)
        self.assertEquals(response.status_code, 200)

    def test_code_find(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')  # test views requires login
        request = HttpRequest()
        request.user = self.user
        request.method = 'POST', 'GET'
        request.session = {}
        response = code_find(request)
        self.assertEquals(response.status_code, 200)