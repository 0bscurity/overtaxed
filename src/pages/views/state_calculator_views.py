import datetime

from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView

from pages.views.state_tax_data import STATE_TAX_DATA


class StateCalculatorView(TemplateView):
    template_name = 'pages/state/state-calculator.html'


class StateTaxCalculateView(View):
    def post(self, request, *args, **kwargs):
        state = request.POST.get("state")
        county = request.POST.get("county")
        resident = request.POST.get("resident") == "on"
        income = float(request.POST.get("income", 0) or 0)
        use_standard_deduction = request.POST.get("use_standard_deduction") == "on"
        deductions = float(request.POST.get("deductions", 0) or 0)
        status = request.POST.get("status", "single")
        tax_year = int(request.POST.get("year", datetime.date.today().year))

        # Fallback to 2024 data if year not found
        tax_data = STATE_TAX_DATA.get(tax_year, STATE_TAX_DATA[2024])

        # Retrieve state-specific tax data
        state_data = tax_data["states"].get(state, {})
        standard_deductions = state_data.get("standard_deductions", {})
        state_tax_brackets = state_data.get("tax_brackets", {}).get(status, [])

        # Retrieve county-specific data
        county_data = state_data.get("counties", {}).get(county, {})
        county_tax_brackets = county_data.get("tax_brackets") or [
            (0, float("inf"), county_data.get("rate", state_data["counties"].get("default", 0)))
        ]

        # Determine standard deduction and taxable income
        standard_deduction = standard_deductions.get(status, 0) if use_standard_deduction else 0
        taxable_income = max(0, income - standard_deduction - deductions)

        # Calculate state tax and marginal rate
        state_tax, state_marginal_rate, state_bracket_breakdown = self.calculate_tax_and_rate(
            taxable_income, state_tax_brackets
        )

        # Calculate county tax and marginal rate
        county_tax, county_marginal_rate, county_bracket_breakdown = self.calculate_tax_and_rate(
            taxable_income, county_tax_brackets
        )

        # Total tax calculation
        total_tax = state_tax + county_tax

        # Calculate rates
        effective_tax_rate = round((total_tax / taxable_income) * 100, 2) if taxable_income > 0 else 0
        marginal_rate = max(state_marginal_rate, county_marginal_rate)

        context = {
            "year": tax_year,
            "tax": total_tax,
            "total_income": int(income),
            "state_tax": int(state_tax),
            "county_tax": int(county_tax),
            "taxable_income": int(taxable_income),
            "deductions": int(deductions),
            "standard_deduction": standard_deduction,
            "effective_tax_rate": effective_tax_rate,
            "marginal_tax_rate": int(marginal_rate * 100),
            "state_bracket_breakdown": state_bracket_breakdown,
            "county_bracket_breakdown": county_bracket_breakdown,
        }

        html = render_to_string("pages/state/state-results.html", context)
        return HttpResponse(html)

    @staticmethod
    def calculate_tax_and_rate(taxable_income, brackets):
        total_tax = 0
        marginal_rate = 0
        bracket_breakdown = []

        for bracket in brackets:
            if len(bracket) == 3:
                lower, upper, rate = bracket
                base_tax = 0
            else:
                lower, upper, rate, base_tax = bracket

            if taxable_income > lower:
                income_in_bracket = min(taxable_income, upper) - lower
                bracket_tax = income_in_bracket * rate + base_tax
                total_tax += bracket_tax
                bracket_breakdown.append({
                    "lower": lower,
                    "upper": upper if upper < float("inf") else "∞",
                    "rate": rate * 100,
                    "income_in_bracket": income_in_bracket,
                    "tax_in_bracket": round(bracket_tax, 2)
                })
                if taxable_income <= upper:
                    marginal_rate = rate
                    break

        return total_tax, marginal_rate, bracket_breakdown


class FetchCountiesView(View):
    def post(self, request, *args, **kwargs):
        state = request.POST.get("state")
        tax_year = int(request.POST.get("year", datetime.date.today().year))

        # Get tax data for the provided year or fallback to default (2024)
        tax_data = STATE_TAX_DATA.get(tax_year, STATE_TAX_DATA[2024])
        state_data = tax_data["states"].get(state, {})

        # Get county names excluding 'default', and transform the names
        counties = [
            {"value": county, "label": county.replace("_", " ").title()}
            for county in state_data.get("counties", {}).keys()
            if county != "default"
        ]

        # Render the county dropdown options HTML using a template
        html = render_to_string("pages/state/county-dropdown.html", {"counties": counties})

        return HttpResponse(html)
