from django.contrib import admin
from catalog.models import ReadingGroup, ReadingGroupEntry
from catalog.models import Collection, CollectionEntry
from catalog.models import Endorsement, EndorsementEntry

# Register your models here.
admin.site.register(ReadingGroup)
admin.site.register(ReadingGroupEntry)
admin.site.register(Collection)
admin.site.register(CollectionEntry)
admin.site.register(Endorsement)
admin.site.register(EndorsementEntry)

