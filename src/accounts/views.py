from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class AccountDetailsView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/account_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
