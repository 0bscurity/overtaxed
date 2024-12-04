from email.policy import default

from django import forms


class FederalTaxForm(forms.Form):
    income = forms.FloatField(
        label="Annual Income ($)",
        min_value=0,
        required=True,
        widget=forms.NumberInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "Enter your income"
        })
    )
    status = forms.ChoiceField(
        label="Filing Status",
        choices=[
            ("single", "Single"),
            ("married", "Married Filing Jointly"),
            ("head_of_household", "Head of Household")
        ],
        widget=forms.Select(attrs={"class": "select select-bordered w-full"})
    )
    deductions = forms.FloatField(
        label="Deductions ($)",
        min_value=0,
        required=False,
        initial=0,
        widget=forms.NumberInput(attrs={
            "class": "input input-bordered w-full",
            "placeholder": "Enter deductions"
        })
    )
    self_employed = forms.BooleanField(
        label="I am self-employed",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "checkbox checkbox-primary"})
    )
    use_standard_deduction = forms.BooleanField(
        label="Use Standard Deduction",
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={"class": "checkbox checkbox-primary"})
    )
