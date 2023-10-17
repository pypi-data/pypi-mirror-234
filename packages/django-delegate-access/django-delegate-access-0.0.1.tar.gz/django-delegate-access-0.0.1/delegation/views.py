from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.module_loading import import_string

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from delegation.models import Delegation
from delegation.serializers import DelegationSerializer

User = get_user_model()


class DelegationViewSet(viewsets.ModelViewSet):
    queryset = Delegation.objects.all()
    serializer_class = DelegationSerializer
    try:
        permission_classes = tuple(import_string(cls) for cls in settings.DELEGATION_PERMISSION_CLASSES)
    except AttributeError:
        permission_classes = []
    http_method_names = ['get', 'post', 'delete']

    def create(self, request, *args, **kwargs):
        delegator_id = request.data.get('delegator')
        delegate_id = request.data.get('delegate')

        st400 = status.HTTP_400_BAD_REQUEST

        # make sure delegator matches logged in user
        if str(request.user.id) != delegator_id:
            return Response({"detail": "Delegator does not match logged in user."}, status=st400)

        # make sure both users aren't the same
        if delegator_id == delegate_id:
            return Response({"detail": "Delegator and delegate cannot be the same user."}, status=st400)

        # make sure delegate exists
        if not User.objects.filter(pk=delegate_id).exists():
            return Response({"detail": "Delegate does not exist."}, status=st400)

        # make sure delegator exists
        if not User.objects.filter(pk=delegator_id).exists():
            return Response({"detail": "Delegator does not exist."}, status=st400)

        # Check if the delegation already exists
        if Delegation.objects.filter(delegator_id=delegator_id, delegate_id=delegate_id).exists():
            return Response({"detail": "Delegation already exists."}, status=st400)

        return super().create(request, *args, **kwargs)

    def destroy(self, request, pk):
        delegator = request.user

        try:
            delegation = Delegation.objects.get(delegator_id=delegator.id, pk=pk)
            delegation.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Delegation.DoesNotExist:
            return Response({"detail": "Delegation does not exist."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def toggle_confirmation(self, request, pk):
        delegation = self.get_object()

        if request.user != delegation.delegator:
            return Response(status=status.HTTP_403_FORBIDDEN)

        delegation.confirmation_enabled = not delegation.confirmation_enabled
        delegation.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
