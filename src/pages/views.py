from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, View

from pages.forms import FederalTaxForm


class HomePageView(TemplateView):
    template_name = 'partials/home.html'


class FederalCalculatorView(TemplateView):
    template_name = "pages/federal/federal-calculator.html"


class FederalTaxCalculateView(View):
    def post(self, request, *args, **kwargs):
        # Get form data
        income = float(request.POST.get("income", 0))
        status = request.POST.get("status", "single")
        deductions = float(request.POST.get("deductions", 0))

        taxable_income = max(0, income - deductions)
        if status == "single":
            tax = taxable_income * 0.22
        elif status == "married":
            tax = taxable_income * 0.20
        elif status == "head_of_household":
            tax = taxable_income * 0.18
        tax = round(tax, 2)

        context = {"tax": tax}
        html = render_to_string("pages/federal/federal-results.html", context)
        return HttpResponse(html)


class StateCalculatorView(TemplateView):
    template_name = 'pages/state-calculator.html'
