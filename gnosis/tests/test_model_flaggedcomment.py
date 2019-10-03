from django.test import TestCase
from catalog.models import FlaggedComment

from django.contrib.auth.models import User

user = User.objects.create_user(username='john',
                                 email='jlennon@beatles.com',
                                 password='glass onion')

class FlaggedCommentModelTest(TestCase):
    def test_object_create(self):
        fl_comment = FlaggedComment()
        fl_comment.comment_id = 1
        fl_comment.description = "test description"
        fl_comment.violation = "unwanted commercial content or spam"
        fl_comment.proposed_by = user

        self.assertEquals(fl_comment.comment_id, 1)
        self.assertEquals(fl_comment.description, "test description")
        self.assertEquals(fl_comment.violation, "unwanted commercial content or spam")
        self.assertEquals(fl_comment.proposed_by.username, 'john')


    def test_create_delete_in_db(self):
        fl_comment = FlaggedComment()
        fl_comment.comment_id = 1
        fl_comment.description = "test description"
        fl_comment.violation = "unwanted commercial content or spam"
        fl_comment.proposed_by = user
        fl_comment.save()

        comments = FlaggedComment.objects.filter(comment_id=1)
        # test object is saved
        self.assertEquals(len(comments), 1)

        comments[0].delete()
        # test object is removed
        comments = FlaggedComment.objects.filter(comment_id=1)
        self.assertEquals(len(comments), 0)



