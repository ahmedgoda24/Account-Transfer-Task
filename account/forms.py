import csv
from django import forms
from .models import Account
from io import TextIOWrapper



class CSVImportForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        file = self.cleaned_data['file']
        try:
            reader = csv.DictReader(TextIOWrapper(file.file, encoding='utf-8'))
            accounts = []
            for i, row in enumerate(reader):
                account_id = row.get('ID')
                name = row.get('Name')
                balance = row.get('Balance')

                # Validate and convert balance
                if not balance:
                    raise forms.ValidationError(f'Balance value cannot be empty at row {i + 1}.')
                
                try:
                    balance = float(balance.replace(',', '.'))
                except ValueError as e:
                    raise forms.ValidationError(f'Invalid balance value at row {i + 1}: {balance}. Error: {e}')
                
             
                accounts.append({'id': account_id, 'name': name, 'balance': balance})
                
            self.cleaned_data['accounts'] = accounts
        except csv.Error as e:
            raise forms.ValidationError(f'Error reading CSV file: {e}')
        
        return file

class TransferFundsForm(forms.Form):
    from_account = forms.ModelChoiceField(
        queryset=Account.objects.all(),
        label='From Account',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    to_account = forms.ModelChoiceField(
        queryset=Account.objects.all(),
        label='To Account',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    amount = forms.DecimalField(
        max_digits=10, decimal_places=2,
        label='Amount',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        from_account = cleaned_data.get('from_account')
        to_account = cleaned_data.get('to_account')
        amount = cleaned_data.get('amount')
        
        if from_account == to_account:
            raise forms.ValidationError("Cannot transfer to the same account.")
        
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        
        if from_account.balance < amount:
            raise forms.ValidationError("Insufficient funds in the source account.")
        
        return cleaned_data


