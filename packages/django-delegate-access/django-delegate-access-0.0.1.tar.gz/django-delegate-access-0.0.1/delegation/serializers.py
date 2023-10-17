from django.contrib.auth import get_user_model
from rest_framework import serializers
from delegation.models import Delegation


class DelegationSerializer(serializers.ModelSerializer):
    delegator_details = serializers.SerializerMethodField()
    delegate_details = serializers.SerializerMethodField()

    class Meta:
        model = Delegation
        fields = ('id', 'delegator', 'delegate', 'token', 'expiration', 'confirmation_enabled', 'created',
                  'delegator_details', 'delegate_details')

    def get_user_details(self, user):
        """Helper method to fetch user id and username."""
        username_field = user.USERNAME_FIELD
        return {
            "id": user.id,
            "username": getattr(user, username_field)
        }

    def get_delegator_details(self, obj):
        return self.get_user_details(obj.delegator)

    def get_delegate_details(self, obj):
        return self.get_user_details(obj.delegate)
