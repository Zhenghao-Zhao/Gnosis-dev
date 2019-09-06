from django.contrib import admin
from catalog.models import ReadingGroup, ReadingGroupEntry
from catalog.models import Collection, CollectionEntry
from catalog.models import Endorsement, EndorsementEntry
from catalog.models import FlaggedComment

from neomodel import db
from catalog.models import Comment

from django.contrib.admin.actions import delete_selected


# Register your models here.
admin.site.register(ReadingGroup)
admin.site.register(ReadingGroupEntry)
admin.site.register(Collection)
admin.site.register(CollectionEntry)
admin.site.register(Endorsement)
admin.site.register(EndorsementEntry)


delete_selected.short_description = "Delete marked flags"

def delete_comment(modeladmin, request, queryset):
    for obj in queryset:
        query = "MATCH (a:Comment) WHERE ID(a)={id} DETACH DELETE a"
        results, meta = db.cypher_query(query, dict(id=obj.comment_id))
        obj.delete()


delete_comment.short_description = "Delete marked flags and their comments"

# define customized interface for flagged comment
class FlaggedCommentAdmin(admin.ModelAdmin):
    exclude = ('comment_id',)
    list_display = ['violation', 'get_comment']
    ordering = ['violation']
    actions = [delete_comment]

    def get_comment(self, obj):
        query = "MATCH (a:Comment) WHERE ID(a)={id} RETURN a"
        results, meta = db.cypher_query(query, dict(id=obj.comment_id))
        comment = None
        if len(results) > 0:
            all_comments = [Comment.inflate(row[0]) for row in results]
            comment = all_comments[0]

        return comment.text
    get_comment.short_description = 'Comment'


admin.site.register(FlaggedComment, FlaggedCommentAdmin)
