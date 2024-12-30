from django.urls import path
from .views import AccountDetailsView

urlpatterns = [
    path('details/', AccountDetailsView.as_view(), name='account_details'),
]
