from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from bookmark.models import Bookmark, BookmarkEntry
from django.urls import reverse
from django.http import HttpResponseRedirect


@login_required
def bookmark(request):

    bookmark = Bookmark.objects.filter(owner=request.user)

    message = None
    print("Bookmark view!")
    return render(
        request, "bookmark.html", {"bookmark": bookmark, "message": message}
    )


@login_required
def bookmark_detail(request, id):

    bookmark = get_object_or_404(Bookmark, pk=id)

    if bookmark.owner == request.user:
        papers = bookmark.papers.order_by('-created_at')
        print(papers)

        return render(request, "bookmark_detail.html", {"bookmark": bookmark,
                                                          "papers": papers, })

    return HttpResponseRedirect(reverse("bookmark"))


@login_required
def bookmark_entry_remove(request, id, eid):
    """Delete view"""
    print("WARNING: Deleting bookmark entry with id {}".format(eid))

    bookmark = get_object_or_404(Bookmark, pk=id)
    if bookmark:
            if bookmark.owner == request.user:
                print("Found bookmark")
                b_entry = get_object_or_404(BookmarkEntry, pk=eid)
                # c_entry = collection.papers.filter(id=eid)
                b_entry.delete()
                print("   ==> Deleted bookmark entry.")
                return HttpResponseRedirect(reverse("bookmark_detail", kwargs={"id": id}))
            else:
                print("Bookmark does not belong to user.")

    return HttpResponseRedirect(reverse("bookmark"))
