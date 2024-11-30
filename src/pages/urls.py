from django.urls import path

from pages.views import HomePageView, FederalCalculatorView, StateCalculatorView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('federal-calculator/', FederalCalculatorView.as_view(), name='federal_calculator'),
    path("state-calculator/", StateCalculatorView.as_view(), name='state_calculator'),
]