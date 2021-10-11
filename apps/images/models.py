import uuid as uuid_lib

from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel

# Create your models here.


def image_directory_path(instance, filename):
    """
    Sets a default path for the image uploads directory.
    """
    return f"images/{instance.account.username}/{instance.uuid}/{filename}"


class Image(TimeStampedModel):
    """
    Model for images uploaded by the users.
    """

    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="images",
        help_text="User account of the owner of the image.",
    )
    image = models.ImageField(upload_to=image_directory_path, help_text="Original image file uploaded by the user.")
    alt = models.CharField(
        max_length=250, null=True, blank=True, help_text="Image description that can be used in HTML `alt` attribute."
    )
    uuid = models.UUIDField(
        db_index=True,
        default=uuid_lib.uuid4,
        editable=False,
        help_text="UUID field used mainly for url lookups of the image.",
    )
