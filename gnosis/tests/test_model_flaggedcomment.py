from django.test import TestCase
from catalog.models import FlaggedComment

from django.contrib.auth.models import User


class FlaggedCommentModelTest(TestCase):

    def setUpTestData(cls):
        user = User.objects.create_user(username='john',
                                        email='jlennon@beatles.com',
                                        password='glass onion')
        # Set up non-modified objects used by all test methods
        FlaggedComment.objects.create(
            comment_id=1,
            description="test description",
            violation="unwanted commercial content or spam",
            proposed_by=user
        )

    def test_object_create(self):
        fl_comment = FlaggedComment.objects.get(id=1)
        self.assertEquals(fl_comment.comment_id, 1)
        self.assertEquals(fl_comment.description, "test description")
        self.assertEquals(fl_comment.violation, "unwanted commercial content or spam")
        self.assertEquals(fl_comment.proposed_by.username, 'john')

    def test_comment_id_label(self):
        fl_comment = FlaggedComment.objects.get(id=1)
        field_label = fl_comment._meta.get_field('comment_id').verbose_name
        self.assertEquals(field_label, 'comment id')

    def test_violation_label(self):
        fl_comment = FlaggedComment.objects.get(id=1)
        field_label = fl_comment._meta.get_field('violation').verbose_name
        self.assertEquals(field_label, 'violation')

    def test_description_label(self):
        fl_comment = FlaggedComment.objects.get(id=1)
        field_label = fl_comment._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')

    def test_created_at_label(self):
        fl_comment = FlaggedComment.objects.get(id=1)
        field_label = fl_comment._meta.get_field('created_at').verbose_name
        self.assertEquals(field_label, 'created at')

    def test_proposed_by_label(self):
        fl_comment = FlaggedComment.objects.get(id=1)
        field_label = fl_comment._meta.get_field('proposed_by').verbose_name
        self.assertEquals(field_label, 'proposed by')

    def test_violation_max_length(self):
        fl_comment = FlaggedComment.objects.get(id=1)
        max_length = fl_comment._meta.get_field('violation').max_length
        self.assertEquals(max_length, 100)

    def test_get_absolute_url(self):
        fl_comment = FlaggedComment.objects.get(id=1)

        # return reverse('paper_detail', args=[str(self.id)])
        self.assertEquals(fl_comment.get_absolute_url(), 'paper/1/')

    def test_create_delete_in_db(self):
        comments = FlaggedComment.objects.filter(comment_id=1)
        # test object is saved
        self.assertEquals(len(comments), 1)

        comments[0].delete()
        # test object is removed
        comments = FlaggedComment.objects.filter(comment_id=1)
        self.assertEquals(len(comments), 0)
