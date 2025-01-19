from django.db.models import Sum
from django.shortcuts import redirect
from django.views.generic import DetailView, FormView, CreateView

from .forms import LGASearchForm
from .models import PollingUnit, AnnouncedPuResults, Lga

# Create your views here.

class PollingUnitResultView(DetailView):
    model = PollingUnit
    template_name = "polling_unit_results.html"
    context_object_name = "polling_unit"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pu_results = AnnouncedPuResults.objects.filter(
            polling_unit_uniqueid=self.object.uniqueid
        )
        context["results"] = pu_results
        return context
    

class LGATotalResultsView(FormView):
    template_name = "lga_total_results.html"
    form_class = LGASearchForm

    def form_valid(self, form):
        lga = form.cleaned_data["lga"]
        lga_polling_units = PollingUnit.objects.filter(lga_id=lga.lga_id)
        total_lga_result = (
            AnnouncedPuResults.objects.filter(
                polling_unit_uniqueid__in=lga_polling_units.values_list(
                    "uniqueid", flat=True
                )
            ).values("party_abbreviation").annotate(total_score=Sum("party_score"))
        )
        return self.render_to_response(
            self.get_context_data(
                form=form,
                results=total_lga_result,
                lga=lga
            )
        )
    

class PollingUnitCreateView(CreateView):
    model = PollingUnit
    template_name = "create_polling_unit.html"
    fields = ["polling_unit_name", "ward_id", "lga_id", "polling_unit_description"]

    def form_valid(self, form):
        polling_unit = form.save()
        return redirect("add_party_results", pk=polling_unit.uniqueid)
    

class AddPartyResultsView(CreateView):
    model = AnnouncedPuResults
    template_name = "add_party_results.html"
    fields = ["party_abbreviation", "party_score"]

    def get_initial(self):
        return {"polling_unit_uniqueid": self.kwargs["pk"]}
