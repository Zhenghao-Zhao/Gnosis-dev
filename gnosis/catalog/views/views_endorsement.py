from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from catalog.models import Endorsement, EndorsementEntry
from django.urls import reverse
from django.http import HttpResponseRedirect
from datetime import date
#
# Endorsement views
#


@login_required
def endorsement_create(request, paper_id):
    """Create an endorsement of a paper, update both databases"""
    user = request.user

    print("AAAAAAAAAAAAAAAAAAAAAAAAAA", request.method)
    if request.method == "POST":
        endorsement_entry = EndorsementEntry()
        endorsement_entry.user = user
        endorsement_entry.paper = paper_id
        endorsement_entry.save()

        try:
            endorsement = Endorsement.objects.filter(paper=paper_id)[0]
            endorsement.endorsement_count += 1
        except:
            endorsement = Endorsement()
            endorsement.endorsement_count = 1
            endorsement.paper = paper_id
        endorsement.save()
        # print("EEEEEEEEEEEEEEEEEEEEEEEEE", Endorsement.objects.filter(paper=paper_id))
    return HttpResponseRedirect(reverse("paper_detail", kwargs={"id": paper_id}))


@login_required
def endorsement_undo(request, paper_id):
    """Undo an endorsement of a paper, update both databases"""
    user = request.user
    if request.method == "POST":
        try:
            endorsement = Endorsement.objects.filter(paper=paper_id)[0]
            endorsement_entry = EndorsementEntry.objects.filter(paper=paper_id, user=user)
            # endorsement.delete()
            endorsement.endorsement_count = max(0, endorsement.endorsement_count-1)
            endorsement.save()
            endorsement_entry.delete()
        except:
            raise ValueError("Invalid Value")
        return HttpResponseRedirect(reverse("paper_detail", kwargs={"id": paper_id}))

    return render(request, "paper_detail.html")

