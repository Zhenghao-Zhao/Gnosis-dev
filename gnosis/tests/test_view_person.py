from django.test import TestCase
from django.contrib.auth.models import User, Permission
from catalog.models import Person
from catalog.views.views_people import person_create, person_update, \
    person_detail, persons, person_find
from django.http import HttpRequest

class PersonViewTest(TestCase):

    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        self.user = User.objects.create_user(
            username='gnosis', email='gnosis@gnosis.com', password='gnosis')

        test_user1.save()
        test_user2.save()

    def test_person_create(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')  # test views requires login
        request = HttpRequest()
        request.user = self.user
        request.method = 'POST'
        request.session = {}
        response = person_create(request)
        self.assertEquals(response.status_code, 200)  # test if response is correct
        self.assertTrue("New Person/Author" in str(response.content) and "First Name*" in str(response.content)
                        and "Last Name*" in str(response.content) and "Affiliation" in str(response.content))

    def test_person_update(self, id):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')  # test views requires login
        request = HttpRequest()
        request.user = self.user
        request.method = 'POST', 'GET'
        request.session = {}
        response = person_update(request, id)
        self.assertEquals(response.status_code, 200)# test if response is correct

    def test_person_detail(self, id):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')  # test views requires login
        request = HttpRequest()
        request.user = self.user
        request.session = {}
        response = person_detail(request, id)
        self.assertEquals(response.status_code, 200)  # test if response is correct

    def test_persons(self):
        request = HttpRequest()
        response = persons(request)
        self.assertEquals(response.status_code, 200)  # test if response is correct

    def test_person_find(self):
        request = HttpRequest()
        request.method = 'POST', 'GET'
        response = person_find(request)
        self.assertEquals(response.status_code, 200)  # test if response is correct


