from django.urls import path
from .views import ImportAccountsView, AccountListView, AccountDetailView, TransferFundsView

urlpatterns = [
    path('import/', ImportAccountsView.as_view(), name='import_accounts'),
    path('accounts/', AccountListView.as_view(), name='list_accounts'),
    path('accounts/<uuid:pk>/', AccountDetailView.as_view(), name='account_detail'),
    path('transfer/', TransferFundsView.as_view(), name='transfer_funds'),
]