from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
import uuid
from django.utils import timezone


class Delegation(models.Model):
    delegator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='delegations_given',
        on_delete=models.CASCADE
    )
    delegate = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='delegations_received',
        on_delete=models.CASCADE
    )
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    expiration = models.DateTimeField(null=True, blank=True)

    confirmation_enabled = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        enforce_expiration = getattr(settings, 'ENFORCE_DELEGATION', False)
        default_days = getattr(settings, 'DEFAULT_DELEGATION_DAYS', None)
        max_days = getattr(settings, 'MAX_DELEGATION_DAYS', None)

        if enforce_expiration and not self.expiration:
            if default_days:
                self.expiration = timezone.now() + timedelta(days=default_days)
            elif max_days:
                self.expiration = timezone.now() + timedelta(days=max_days)
            else:
                # This situation should not arise as we're enforcing expiration,
                # one of default or max days should be set.
                raise ValidationError("Expiration date is required due to ENFORCE_DELEGATION setting.")

        elif self.expiration and max_days:
            max_expiration = timezone.now() + timedelta(days=max_days)
            if self.expiration > max_expiration:
                self.expiration = max_expiration

        super(Delegation, self).save(*args, **kwargs)

    def __str__(self):
        if self.expiration:
            return f'{self.delegator} delegates to {self.delegate} until {self.expiration}'
        else:
            return f'{self.delegator} delegates to {self.delegate} forever'
