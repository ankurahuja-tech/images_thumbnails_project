from django.contrib.postgres.fields import ArrayField, IntegerRangeField
from django.core.validators import MinValueValidator
from django.db import models

from apps.core.models import TimeStampedModel

# Create your models here.


class Plan(TimeStampedModel):
    """
    Base model for account tiers (user plans).
    """

    name = models.CharField(max_length=50, help_text="Name of the account tier.")
    available_thumbnail_heights = ArrayField(
        base_field=models.PositiveSmallIntegerField(),
        null=True,
        blank=True,
        help_text="This is a list of available thumbnail heights in pixels (px).",
    )
    can_access_original_image = models.BooleanField(help_text="Ability to access original image.")
    can_fetch_expiring_link = models.BooleanField(
        help_text="Ability to fetch a link that expires after a number of seconds."
    )
    expiring_link_time_range = IntegerRangeField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        help_text="Minimum and maximum number of seconds for the expiring link to expire. To be specified by user.",
    )

    def __str__(self):
        return self.name
