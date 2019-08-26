from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Bookmark, BookmarkEntry
from django.urls import reverse
from django.http import HttpResponseRedirect




@login_required
def bookmark_detail(request, id):

    bookmark = Bookmark.objects.filter(pk=id)

    if bookmark.owner == request.user:
        papers = bookmark.papers.order_by('-created_at')
        print(papers)

        return render(request, "bookmark.html", {"bookmark": bookmark,
                                                            "papers": papers, })

    return HttpResponseRedirect(reverse("bookmark"))


@login_required
def bookmark_entry_remove(request, id, eid):
    """Delete view"""
    print("WARNING: Deleting bookmark entry with eid {}".format(eid))

    # check if the bookmark for the user exists, if not, create one
    try:
        bookmark = get_object_or_404(Bookmark, pk=id)
    except:
        bookmark = Bookmark()
        bookmark.owner = request.user

    if bookmark.owner == request.user:
        print("Found bookmark")
        try:
            b_entry = get_object_or_404(BookmarkEntry, pk=eid)
            b_entry.delete()
        except:
            print("   ==> No such entry.")
        return HttpResponseRedirect(reverse("bookmark_detail", kwargs={"id": id}))
    else:
        print("Bookmark does not belong to user.")

    return HttpResponseRedirect(reverse("bookmark"))
