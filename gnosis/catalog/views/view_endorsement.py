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
def endorsement_create(request):
    """Create an endorsement of a paper, update both databases"""
    user = request.user

    paper = request.paper
    if request.method == "POST":
        endorsement_entry = EndorsementEntry()
        endorsement_entry.user = user
        endorsement_entry.paper = paper

        try:
            endorsement = Endorsement.objects.get(pk=paper)
            endorsement.endorsement_count += 1
        except:
            endorsement = Endorsement()
            endorsement.endorsement_count = 1
            endorsement.paper = paper
        return HttpResponseRedirect(reverse("endorsement_create"))
    return render(request, "paper_detail.html")
