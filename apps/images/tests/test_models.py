import os

import pytest
from django.conf import settings
from django.core.files.storage import default_storage

from apps.images.models import Image


class TestImage:
    def test_create_image(self, image_premium_account_fixture):
        """
        Assert that the Image instance exists.
        """
        test_image = image_premium_account_fixture
        assert Image.objects.all().count() == 1
        assert test_image.image.name.endswith("image.jpg")

    def test_image_directory_path(self, image_premium_account_fixture, account_premium_fixture):
        """
        Assert that the Image instance's image file exists at the desired directory.
        """
        desired_path = os.path.join(
            settings.MEDIA_ROOT,
            f"images/{account_premium_fixture.username}/{image_premium_account_fixture.uuid}/image.jpg",
        )
        assert default_storage.exists(desired_path)
