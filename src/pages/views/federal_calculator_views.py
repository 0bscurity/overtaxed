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
        income = float(request.POST.get("income", 0) or 0)
        self_employment_income = float(request.POST.get("self_employment_income", 0) or 0)
        status = request.POST.get("status", "single")
        use_standard_deduction = request.POST.get("use_standard_deduction") == "on"

        # Define standard deductions
        standard_deductions = {
            "single": 14600,
            "married": 29200,
            "head_of_household": 21900,
        }

        # Apply standard deduction if selected
        if use_standard_deduction:
            deductions = standard_deductions[status]
        else:
            deductions = float(request.POST.get("deductions", 0) or 0)

        # Combine all income for regular tax calculation
        total_income = income + self_employment_income

        # Calculate the taxable portion of self-employment income (92.35%)
        self_employment_taxable_income = self_employment_income * 0.9235
        self_employment_non_taxable_income = self_employment_income - self_employment_taxable_income

        # Calculate self-employment tax
        self_employment_tax = self_employment_taxable_income * 0.153

        # Adjust taxable income for regular tax brackets by deducting half of self-employment tax
        adjusted_income = income + self_employment_taxable_income

        taxable_income = max(0, adjusted_income - deductions)

        # Define tax brackets
        brackets = {
            "single": [
                (0, 11600, 0.10),
                (11601, 47150, 0.12),
                (47151, 100525, 0.22),
                (100526, 191950, 0.24),
                (191951, 243725, 0.32),
                (243726, 609350, 0.35),
                (609351, float("inf"), 0.37),
            ],
            "married": [
                (0, 23200, 0.10),
                (23201, 94300, 0.12),
                (94301, 201050, 0.22),
                (201051, 383900, 0.24),
                (383901, 487450, 0.32),
                (487451, 731200, 0.35),
                (731201, float("inf"), 0.37),
            ],
            "head_of_household": [
                (0, 16550, 0.10),
                (16551, 63100, 0.12),
                (63101, 100500, 0.22),
                (100501, 191950, 0.24),
                (191951, 243700, 0.32),
                (243701, 609350, 0.35),
                (609351, float("inf"), 0.37),
            ],
        }

        # Calculate regular income tax
        regular_tax = 0
        tax_breakdown = []
        for lower, upper, rate in brackets[status]:
            if taxable_income > lower:
                income_in_bracket = min(taxable_income, upper) - lower
                bracket_tax = income_in_bracket * rate
                regular_tax += bracket_tax
                tax_breakdown.append({
                    "amount": int(income_in_bracket),
                    "rate": int(rate * 100),
                    "tax": int(bracket_tax),
                })

        # Total tax is the sum of regular tax and self-employment tax
        total_tax = round(regular_tax + self_employment_tax, 2)

        context = {
            "tax": total_tax,
            "total_income": int(total_income),
            "regular_tax": int(regular_tax),
            "self_employment_tax": int(self_employment_tax),
            "taxable_income": int(taxable_income),
            "deductions": int(deductions),
            "self_employment_non_taxable_income": int(self_employment_non_taxable_income),
            "tax_breakdown": tax_breakdown,
        }
        html = render_to_string("pages/federal/federal-results.html", context)
        return HttpResponse(html)


class StateCalculatorView(TemplateView):
    template_name = 'pages/state-calculator.html'
