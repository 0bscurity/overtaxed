import datetime

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import TemplateView, View

from pages.views.tax_data import TAX_DATA


class HomePageView(TemplateView):
    template_name = 'partials/home.html'


class FederalCalculatorView(TemplateView):
    template_name = "pages/federal/federal-calculator.html"


class FederalTaxCalculateView(View):
    def post(self, request, *args, **kwargs):
        income = float(request.POST.get("income", 0) or 0)
        self_employed = request.POST.get("self_employed") == "on"
        self_employment_income = 0
        if self_employed:
            self_employment_income = float(request.POST.get("self_employment_income", 0) or 0)
        status = request.POST.get("status", "single")
        use_standard_deduction = request.POST.get("use_standard_deduction") == "on"
        deductions = float(request.POST.get("deductions", 0) or 0)
        tax_year = int(request.POST.get("year", datetime.date.today().year))

        # Fallback to 2024 data if year not found
        tax_data = TAX_DATA.get(tax_year, TAX_DATA[2024])

        standard_deductions = tax_data["standard_deductions"]
        tax_brackets = tax_data["tax_brackets"]

        # Calculate income
        total_income, self_employment_taxable_income, self_employment_non_taxable_income = self.get_total_income(
            income, self_employment_income
        )
        self_employment_tax = self.calculate_self_employment_tax(self_employment_taxable_income)

        # Determine standard deduction and taxable income
        standard_deduction = standard_deductions.get(status, 0) if use_standard_deduction else 0
        taxable_income = max(0, total_income - standard_deduction - deductions - self_employment_non_taxable_income)

        federal_tax, marginal_rate, bracket_breakdown = self.calculate_federal_tax(taxable_income, tax_brackets[status])

        total_tax = round(federal_tax + self_employment_tax, 2)

        # Calculate rates
        effective_tax_rate = round((total_tax / taxable_income) * 100, 2) if taxable_income > 0 else 0

        context = {
            "year": datetime.date.today().year,
            "tax": total_tax,
            "total_income": int(total_income),
            "federal_tax": int(federal_tax),
            "self_employment_tax": int(self_employment_tax),
            "self_employment_non_taxable_income": self_employment_non_taxable_income,
            "taxable_income": int(taxable_income),
            "deductions": int(deductions),
            "standard_deduction": standard_deduction,
            "effective_tax_rate": effective_tax_rate,
            "marginal_tax_rate": int(marginal_rate * 100),
            "bracket_breakdown": bracket_breakdown,
        }

        html = render_to_string("pages/federal/federal-results.html", context)
        return HttpResponse(html)

    @staticmethod
    def get_total_income(income, self_employment_income):
        self_employment_taxable_income = self_employment_income * 0.9235 if self_employment_income > 0 else 0
        self_employment_non_taxable_income = self_employment_income - self_employment_taxable_income
        total_income = income + self_employment_income
        return total_income, self_employment_taxable_income, self_employment_non_taxable_income

    @staticmethod
    def calculate_self_employment_tax(self_employment_taxable_income):
        return self_employment_taxable_income * 0.153 if self_employment_taxable_income > 0 else 0

    @staticmethod
    def calculate_federal_tax(taxable_income, brackets):
        federal_tax = 0
        marginal_rate = 0
        bracket_breakdown = []

        for lower, upper, rate in brackets:
            if taxable_income > lower:
                income_in_bracket = min(taxable_income, upper) - lower
                bracket_tax = income_in_bracket * rate
                federal_tax += bracket_tax
                bracket_breakdown.append({
                    "lower": lower,
                    "upper": upper if upper < float('inf') else "∞",
                    "rate": rate * 100,
                    "income_in_bracket": income_in_bracket,
                    "tax_in_bracket": round(bracket_tax, 2)
                })
                if taxable_income <= upper:
                    marginal_rate = rate
                    break

        return federal_tax, marginal_rate, bracket_breakdown
