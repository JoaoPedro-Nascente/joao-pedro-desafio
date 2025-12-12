from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from datetime import date
from uuid import uuid4

from ..models import Transaction, TypeTransaction
from .views import summary_view, transaction_list_create, create_summary, get_filtered_transactions

#Unit test for views helpers
class HelpersTestCase(TestCase):
    def setUp(self):
        self.username_a = 'testUser_a'
        self.password_a = 'testPassword_b'
        self.user = User.objects.create_user(username=self.username_a, password=self.password_a)

        Transaction.objects.create(user=self.user, description="Salario", amount=5000.00, type="income", date=date(2025, 1, 1))
        Transaction.objects.create(user=self.user, description="Aluguel", amount=1500.00, type="expense", date=date(2025, 1, 5))
        Transaction.objects.create(user=self.user, description="Conta de Luz", amount=200.00, type="expense", date=date(2025, 1, 10))
        Transaction.objects.create(user=self.user, description="Freelance", amount=1000.00, type="income", date=date(2025, 1, 15))

    #create_summary()
    def test_create_summary(self):
        data = create_summary(self.user)
        '''
        Income: 6000.00
        Outcome: 1700.00
        Net Balance: 4300.00
        '''
        self.assertEqual(data['total_income'], Decimal('6000.00'))
        self.assertEqual(data['total_expense'], Decimal('1700.00'))
        self.assertEqual(data['net_balance'], Decimal('4300.00'))

    #get_filtered_transactions()
    def test_filter_by_type(self):
        params = {'type': 'income'}
        filtered_transactions = get_filtered_transactions(params, self.user)

        self.assertEqual(filtered_transactions.count(), 2)
        self.assertTrue(all(t.type == 'income' for t in filtered_transactions))

    def test_filter_by_description(self):
        params = {'description': 'aluguel'}
        filtered_transactions = get_filtered_transactions(params, self.user)

        self.assertEqual(filtered_transactions.count(), 1)
        self.assertEqual(filtered_transactions.first().description.lower(), "aluguel")


#Views unit tests
class TransactionAPITestCase(APITestCase):
    def setUp(self):
        self.username_a = 'testUser_a'
        self.password_a = 'testPassword_b'
        self.user = User.objects.create_user(username=self.username_a, password=self.password_a)

        login_response = self.client.post(
            reverse('token_obtain_pair'),
            {'username': self.username_a, 'password': self.password_a},
            format='json'
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK, "Failed to obtain token.")
        self.access_token = login_response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.list_create_url = reverse('transaction_list_create')
        self.summary_url = reverse('summary_view')

        self.test_transaction = Transaction.objects.create(
            user=self.user,
            description='Teste',
            amount=111.11,
            type='expense',
            date='2025-12-01'
        )

        self.transactions_manager_url = reverse('transactions_manager', args=[self.test_transaction.id])

        #Creates 15 objects (counting with the 'Teste' one) varying between expense and income
        for i in range(1, 15):
            Transaction.objects.create(
            user=self.user,
            description=f'Item {i}',
            amount=Decimal(i),
            type='expense' if i % 2 == 0 else 'income',
            date=date(2025, 11, i % 28 + 1)
            )

        self.valid_data = {
            'user': self.user.id,
            'description': 'Novo Teste Valido',
            'amount': 250.50,
            'type': 'income',
            'date': '2025-12-01'
        }

        self.invalid_data = {
            'user': self.user.id,
            'description': 'Erro',
            'amount': -250.50, #Should not be accepted amount < 0
            'type': 'income',
            'date': '2025-12-01'
        }

        self.username_b = 'testUser_b'
        self.password_b = 'testPassword_b'
        self.user_b = User.objects.create_user(username=self.username_b, password=self.password_b)

        self.transaction_user_b = Transaction.objects.create(
            user=self.user_b,
            description='Transacao usuario b',
            amount=500.00,
            type='expense',
            date='2025-12-31'
        )

        self.transactions_manager_other_url = reverse('transactions_manager', args=[self.transaction_user_b.id])

    #model test
    def test_model_representation_str(self):
        expected_str = f'Teste, , 2025-12-01, valor: R$111.11, tipo: expense'

        self.assertEqual(str(self.test_transaction).split(',')[0], expected_str.split(',')[0])

    #transactions_manager()
    # ['POST']
    def test_create_transaction_success(self):
        initial_count = Transaction.objects.count()
        response = self.client.post(self.list_create_url, self.valid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), initial_count+1)
        self.assertEqual(response.data['description'], self.valid_data['description'])

    def test_create_transaction_fail(self):
        initial_count = Transaction.objects.count()
        response = self.client.post(self.list_create_url, self.invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Transaction.objects.count(), initial_count)

    #Pagination
    def test_pagination_default(self):
        response = self.client.get(self.list_create_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 15)
        self.assertEqual(len(response.data['results']), 10)
        self.assertIn('next', response.data)

    def test_pagination_custom_size(self):
        response = self.client.get(self.list_create_url, {'page_size': 5})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)

    def test_filter_combined_pagination(self):
        response = self.client.get(self.list_create_url, {'type': TypeTransaction.INCOME})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 7)
        self.assertEqual(len(response.data['results']), 7)

    #transactions_manager()['GET']
    def test_get_transaction_by_id_success(self):
        response = self.client.get(self.transactions_manager_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], self.test_transaction.description)

    def test_get_transaction_by_id_fail(self):
        invalid_id = uuid4()
        self.assertFalse(Transaction.objects.filter(pk=invalid_id).exists(), f"Existe Transaction com id {invalid_id}")

        fail_request_url = reverse('transactions_manager', args=[invalid_id])

        response = self.client.get(fail_request_url)
        self.assertEqual(response.data, status.HTTP_404_NOT_FOUND)

    def test_get_transaction_by_id_fail_other_user(self):
        response = self.client.get(self.transactions_manager_other_url)
        
        self.assertEqual(response.data, status.HTTP_404_NOT_FOUND)
        
        self.assertNotContains(response, self.transaction_user_b.description)

    def test_list_transactions_only_shows_own_data(self):
        response = self.client.get(self.list_create_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 15) 
        
        self.assertNotContains(response, self.transaction_user_b.description)

    #transactions_manager()['PUT', 'PATCH']
    def test_update_transaction_full_put(self):
        new_data = {
            'description': 'PUT',
            'amount': 999.99,
            'type': TypeTransaction.INCOME,
            'date': '2026-01-01'
        }
        response = self.client.put(self.transactions_manager_url, new_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.test_transaction.refresh_from_db()
        self.assertEqual(self.test_transaction.description, 'PUT')

    def test_update_transaction_partial_patch(self):
        partial_data = {"description": "PATCH"}
        response = self.client.patch(self.transactions_manager_url, partial_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.test_transaction.refresh_from_db()
        self.assertEqual(self.test_transaction.description, "PATCH")
        self.assertEqual(self.test_transaction.amount, Decimal('111.11'))

    def test_update_other_user_data_fails(self):
        data_to_update = {'description': 'It must fail'}
        
        response = self.client.put(self.transactions_manager_other_url, data_to_update, format='json')
        
        self.assertEqual(response.data, status.HTTP_404_NOT_FOUND)
        
        self.transaction_user_b.refresh_from_db()
        self.assertNotEqual(self.transaction_user_b.description, 'It must fail')

    #transactions_manager()['DELETE']
    def test_delete_transaction_success(self):
        initial_count = Transaction.objects.count()
        response = self.client.delete(self.transactions_manager_url)
        
        self.assertEqual(response.data, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Transaction.objects.count(), initial_count - 1)

    def test_delete_other_user_data_fails(self):
            initial_count = Transaction.objects.count()
            
            response = self.client.delete(self.transactions_manager_other_url)
            
            self.assertEqual(response.data, status.HTTP_404_NOT_FOUND)
            
            self.assertEqual(Transaction.objects.count(), initial_count)

    #Test for authenticated routes
    def test_access_denied_without_token(self):
            self.client.credentials() 
            
            response = self.client.get(self.list_create_url)
            
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertIn('Authentication credentials were not provided', str(response.data))

            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    #Summary
    def test_get_summary_success(self):
        response = self.client.get(self.summary_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertIn('net_balance', response.data)
        self.assertIn('total_income', response.data)
        
        self.assertEqual(response.data['net_balance'], '-118.11') 
        self.assertEqual(response.data['total_income'], '49.00')