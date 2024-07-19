from io import TextIOWrapper
from django.views.generic import View,ListView, DetailView

from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.db import transaction
from django.shortcuts import redirect, render
import csv
from .models import Account
from .forms import CSVImportForm, TransferFundsForm



class ImportAccountsView(FormView):
    template_name = 'import_accounts.html'
    form_class = CSVImportForm
    success_url = reverse_lazy('list_accounts')

    def form_valid(self, form):
        accounts = form.cleaned_data['accounts']
        
        for account_data in accounts:
            try:
                Account.objects.create(
                    id=account_data['id'],
                    name=account_data['name'],
                    balance=account_data['balance']
                )
            except Exception as e:
                form.add_error('file', f'Error creating account: {e}')
                return self.form_invalid(form)
        
        return super().form_valid(form)        
class AccountListView(ListView):
    model = Account
    template_name = 'list_accounts.html'
    context_object_name = 'accounts'
    paginate_by = 10

class AccountDetailView(DetailView):
    model = Account
    template_name = 'account_detail.html'
    context_object_name = 'account'


class TransferFundsView(View):
    template_name = 'transfer_funds.html'
    
    def get(self, request):
        form = TransferFundsForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = TransferFundsForm(request.POST)
        if form.is_valid():
            from_account = form.cleaned_data['from_account']
            to_account = form.cleaned_data['to_account']
            amount = form.cleaned_data['amount']
            
            # Perform the transfer within an atomic transaction
            with transaction.atomic():
                from_account.balance -= amount
                to_account.balance += amount
                from_account.save()
                to_account.save()
            
            return redirect('list_accounts')
        return render(request, self.template_name, {'form': form})
