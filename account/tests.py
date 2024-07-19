from django.test import TestCase
import unittest
from django.test import TestCase
from django.urls import reverse
from django.test import Client
from django.test import TestCase, RequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from .views import ImportAccountsView
from .forms import CSVImportForm
from .models import Account



class ImportAccountsViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = ImportAccountsView.as_view()
        
    def test_valid_account_creation(self):
        csv_file = SimpleUploadedFile('valid_data.csv', b'ID,Name,Balance\n1,John Doe,100.00')
        request = self.factory.post('/import_accounts/', {'file': csv_file})
        response = self.view(request)
        self.assertEqual(response.status_code, 302)  # Redirecting to success url
        
        # Check if account was created
        self.assertEqual(Account.objects.count(), 1)
    
    def test_error_handling_on_account_creation(self):
        csv_file = SimpleUploadedFile('invalid_data.csv', b'ID,Name,Balance\n1,John Doe,invalid_balance')
        request = self.factory.post('/import_accounts/', {'file': csv_file})
        response = self.view(request)
        
        self.assertEqual(response.status_code, 200)  # Form is invalid
        self.assertFormError(response, 'form', 'file', 'Error creating account: could not convert string to float')


class TestTransferFundsView(TestCase):
    
    def setUp(self):
        self.client = Client()

    def test_valid_transfer(self):
        response = self.client.post(reverse('transfer_funds'), {
            'from_account': 'Test Account 1',
            'to_account': 'Test Account 2',
            'amount': 100.00
        })
        self.assertEqual(response.status_code, 302)  # Check if it redirects after successful transfer

    def test_invalid_form_submission_missing_fields(self):
        response = self.client.post(reverse('transfer_funds'), {})
        self.assertEqual(response.status_code, 200)  # Check if it stays on the same page

    def test_invalid_form_submission_insufficient_funds(self):
        response = self.client.post(reverse('transfer_funds'), {
            'from_account': 'Test Account 1',
            'to_account': 'Test Account 2',
            'amount': 999999.00  # Assuming this amount exceeds the balance
        })
        self.assertEqual(response.status_code, 200)  # Check if it stays on the same page

if __name__ == '__main__':
    unittest.main()


