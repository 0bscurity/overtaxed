from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'partials/home.html'


class FederalCalculatorView(TemplateView):
    template_name = 'pages/federal-calculator.html'


class StateCalculatorView(TemplateView):
    template_name = 'pages/state-calculator.html'
