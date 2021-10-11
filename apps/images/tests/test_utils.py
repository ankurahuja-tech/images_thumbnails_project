import os

import PIL
import pytest
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.images.api.utils import create_thumbnail


class TestCreateThumbnail:
    def test_create_thumbnail(self, account_premium_fixture, image_premium_account_fixture):
        """
        Assert that `create_thumbnail` function creates image file of correct size and format at the desired location.
        """
        source_image_file = SimpleUploadedFile(
            name="test_image.jpg",
            content=open(os.path.join(settings.BASE_DIR, "test_media_files/test_image.jpg"), "rb").read(),
            content_type="image/jpeg",
        )
        request_height = 100
        thumbnail_file_path = os.path.join(
            settings.MEDIA_ROOT,
            f"images/{account_premium_fixture}/{image_premium_account_fixture.uuid}/\
                {request_height}-{image_premium_account_fixture.uuid}.jpg",
        )

        create_thumbnail(image_file=source_image_file, height=request_height, path=thumbnail_file_path)

        img = PIL.Image.open(thumbnail_file_path)

        assert open(thumbnail_file_path, "rb").read()
        assert img.format == "JPEG"
        assert img.height == request_height
