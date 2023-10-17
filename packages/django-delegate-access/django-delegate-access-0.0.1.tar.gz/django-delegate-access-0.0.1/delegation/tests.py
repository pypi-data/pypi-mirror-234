from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from delegation.models import Delegation

User = get_user_model()


class DelegationViewTest(TestCase):

    def setUp(self):
        delegator = User.objects.create_user(username='delegator', password='testpass123', id=1)
        delegate = User.objects.create_user(username='delegate', password='testpass123', id=2)

        self.delegator = delegator
        self.delegate = delegate
        self.client = APIClient()

    def test_create_delegation(self):
        self.client.force_authenticate(self.delegator)

        data = {
            'delegate': self.delegate.id,
            'delegator': self.delegator.id
        }
        response = self.client.post('/delegation/delegations/', data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Delegation.objects.filter(delegator=self.delegator, delegate=self.delegate).exists())

    def test_toggle_confirmation(self):
        delegation = Delegation.objects.create(delegator=self.delegator, delegate=self.delegate)
        self.client.force_authenticate(self.delegator)
        response = self.client.get(f'/delegation/delegations/{delegation.id}/toggle_confirmation/')
        self.assertEqual(response.status_code, 204)
        delegation.refresh_from_db()
        self.assertFalse(delegation.confirmation_enabled)

    def test_delete_delegation(self):
        delegation = Delegation.objects.create(delegator=self.delegator, delegate=self.delegate)
        self.client.force_authenticate(self.delegator)
        url = f'/delegation/delegations/{delegation.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Delegation.objects.filter(pk=delegation.id).exists())

    def test_unauthorized_toggle_confirmation(self):
        delegation = Delegation.objects.create(delegator=self.delegator, delegate=self.delegate)
        self.client.force_authenticate(self.delegate)  # Wrong user authenticated
        response = self.client.get(f'/delegation/delegations/{delegation.id}/toggle_confirmation/')
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_unauthorized_delete_delegation(self):
        delegation = Delegation.objects.create(delegator=self.delegator, delegate=self.delegate)
        self.client.force_authenticate(self.delegate)  # Wrong user authenticated
        response = self.client.delete(f'/delegation/delegations/{delegation.id}/')
        self.assertEqual(response.status_code, 404)  # Forbidden

    def test_toggle_confirmation_non_existent_delegation(self):
        non_existent_delegation_id = 9999
        self.client.force_authenticate(self.delegator)
        response = self.client.get(f'/delegation/delegations/{non_existent_delegation_id}/toggle_confirmation/')
        self.assertEqual(response.status_code, 404)  # Not Found

    def test_delete_non_existent_delegation(self):
        non_existent_delegation_id = 9999
        self.client.force_authenticate(self.delegator)
        response = self.client.delete(f'/delegation/delegations/{non_existent_delegation_id}/')
        self.assertEqual(response.status_code, 404)  # Not Found


