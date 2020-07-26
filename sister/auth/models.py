import uuid
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False
        )

    first_name = None
    last_name = None
    
    def get_full_name(self):
        """
        Return the fullname.
        """
        return self.profile.full_name

    def get_short_name(self):
        """Return the short name for the user."""
        return self.profile.short_name