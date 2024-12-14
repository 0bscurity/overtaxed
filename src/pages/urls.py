from django.urls import path

from pages.views.federal_calculator_views import HomePageView, FederalCalculatorView, FederalTaxCalculateView
# from pages.views.login import LoginView
from pages.views.state_calculator_views import StateCalculatorView, StateTaxCalculateView, FetchCountiesView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),

    # path('accounts/login/', LoginView.as_view(), name='login'),

    path('federal-calculator/', FederalCalculatorView.as_view(), name='federal_calculator'),
    path('federal-calculator/calculate/', FederalTaxCalculateView.as_view(), name='federal_tax_calculate'),

    path('state-calculator/', StateCalculatorView.as_view(), name='state_calculator'),
    path('state-calculator/calculate/', StateTaxCalculateView.as_view(), name='state_tax_calculate'),
    path('state-calculator/fetch-counties/', FetchCountiesView.as_view(), name='fetch_counties'),
]
