from django.urls import path

from pages.views import HomePageView, FederalCalculatorView, StateCalculatorView, FederalTaxCalculateView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('federal-calculator/', FederalCalculatorView.as_view(), name='federal_calculator'),
    path('federal-calculator/calculate/', FederalTaxCalculateView.as_view(), name='federal_tax_calculate'),

    path("state-calculator/", StateCalculatorView.as_view(), name='state_calculator'),
]