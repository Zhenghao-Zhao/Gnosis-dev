from django.test import TestCase
from django.urls import reverse

from catalog.models import FlaggedComment, Paper

from django.contrib.auth.models import User
from django.http import HttpRequest


class FlaggedCommentViewTest(TestCase):
    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        self.user = User.objects.create_user(
            username='gnosis', email='gnosis@gnosis.com', password='gnosis')

        test_user1.save()
        test_user2.save()

        # Create a paper at server
        paper = Paper()
        paper.title = "No title"
        paper.abstract = "The abstract is missing."
        paper.keywords = ""
        paper.download_link = "https://google.com"
        paper.id = "01"
        paper.save()


    # def test_fl_form

    def test_fl_form_redirect(self):

        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        fl_form_data = {
            'violation': 'unwanted commercial content or spam',
            'description': 'test description'
        }

        # test POST request
        response = self.client.post(reverse('paper_detail', kwargs={'id': '01'}), fl_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('paper_detail'))



