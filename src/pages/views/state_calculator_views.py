from django.views.generic import TemplateView


class StateCalculatorView(TemplateView):
    template_name = 'pages/state-calculator.html'
