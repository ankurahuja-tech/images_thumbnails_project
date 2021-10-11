from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.plans.models import Plan

# Create your models here.


class Account(AbstractUser):
    """
    Base model for a user account.
    """

    plan = models.ForeignKey(
        Plan,
        null=True,
        blank=True,
        default=1,  # NOTE: Assumes the default user plan in database has id = 1.
        help_text="Chosen account tier (user plan).",
        on_delete=models.SET_DEFAULT,
        related_name="accounts",
    )
