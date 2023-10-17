from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone

from delegation.models import Delegation


class DelegationTokenAuthentication(TokenAuthentication):

    def authenticate(self, request):
        # Call the parent class's authenticate
        auth_result = super().authenticate(request)

        # If no authentication information is provided, return None
        if auth_result is None:
            return None

        user, auth_token = auth_result
        user, auth_token = self.custom_authenticate_credentials(auth_token.key, request)
        return user, auth_token

    def custom_authenticate_credentials(self, key, request):
        # Regular token check for the delegate (the user requesting to act on behalf of another)
        delegate, token = super().authenticate_credentials(key)

        # Get the active user model
        User = get_user_model()

        # Check for initial act-as request
        act_as_username = request.headers.get('Act-As-Username')
        if act_as_username:
            try:
                delegator = User.objects.get(username=act_as_username)

                # Verify the delegation permission
                if not Delegation.objects.filter(delegator=delegator, delegate=delegate).exists():
                    raise AuthenticationFailed('Delegate does not have permission to act as the specified user.')

                # Create a new delegation token for this session
                delegation = Delegation.objects.create(delegator=delegator, delegate=delegate)
                request.new_delegation_token = delegation.token
                return delegate, token

            except User.DoesNotExist:
                raise AuthenticationFailed('User specified in Act-As-Username does not exist.')

        # Check for delegation token in subsequent requests
        delegation_token = request.headers.get('Delegation-Token')
        if delegation_token:
            try:
                delegation = Delegation.objects.get(token=delegation_token)

                # Ensure the delegation is valid and not expired
                if delegation.expiration and delegation.expiration <= timezone.now():
                    raise AuthenticationFailed('Delegation has expired.')

                return delegation.delegator, token

            except Delegation.DoesNotExist:
                raise AuthenticationFailed('Invalid delegation token.')

        return delegate, token
