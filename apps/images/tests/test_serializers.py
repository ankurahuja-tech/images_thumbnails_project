import pytest
from django.conf import settings
from rest_framework.exceptions import ValidationError

from apps.images.api.serializers import ImageSerializer


class TestImageSerializer:

    # General serializer tests

    def test_serialize_model(self, image_premium_account_fixture):
        """
        Assert that the serializer correctly serializes Image model instance.
        """
        serializer = ImageSerializer(image_premium_account_fixture)

        assert serializer.data

    def test_contains_expected_fields(self, image_premium_account_fixture):
        """
        Assert that the serialized Image data contain all the correct fields, including `thumbnails` field.
        """
        serializer = ImageSerializer(image_premium_account_fixture)
        base_fields = ["id", "account", "image", "alt", "uuid"]
        to_representation_fields = ["thumbnails"]  # field added from "to representation" Image method

        assert set(serializer.data.keys()) == set(base_fields + to_representation_fields)

    # Validation tests

    def test_deserialize_valid_data(self, image_serializer_valid_data_fixture):
        """
        Assert that the serializer correctly turns valid serialized data into a model (i.e. deserialize).
        """
        serializer = ImageSerializer(data=image_serializer_valid_data_fixture)

        assert serializer.is_valid(raise_exception=True)
        assert serializer.errors == {}

    def test_deserialize_invalid_data(self, image_serializer_invalid_data_fixture):
        """
        Assert that the serializer correctly raises ValidationError exception when given unsupported
        image file extension (GIF).
        """
        serializer = ImageSerializer(data=image_serializer_invalid_data_fixture)

        assert not serializer.is_valid()
        assert pytest.raises(ValidationError)

    # `to_representation` method tests

    def test_original_image_link_authorized(self, image_premium_account_fixture, account_premium_fixture):
        """
        Assert that an authorized user gets link to the original uploaded image file.
        """
        serializer = ImageSerializer(image_premium_account_fixture)

        assert serializer.data["image"] == image_premium_account_fixture.image.url

    def test_original_image_link_unauthorized(self, image_basic_account_fixture):
        """
        Assert that an unauthorized user does not get a link to the original uploaded image file.
        """
        serializer = ImageSerializer(image_basic_account_fixture)

        assert serializer.data["image"] == "Original image is not available for your user plan."

    def test_thumbnail_links_authorized(
        self,
        image_basic_account_fixture,
        image_premium_account_fixture,
        account_basic_fixture,
        account_premium_fixture,
    ):
        """
        Assert that Image serializer `to_representation` method correctly adds thumbnails based on user plan.
        Test includes Basic and Premium plan.
        """
        # Basic plan - one thumbnail link
        serializer = ImageSerializer(image_basic_account_fixture)
        basic_available_thumbnail_heights = account_basic_fixture.plan.available_thumbnail_heights
        basic_available_thumbnails = {}
        for height in basic_available_thumbnail_heights:
            basic_available_thumbnails[f"{height}px"] = (
                settings.DEFAULT_MEDIA_DOMAIN + f"/api/v1/images/{image_basic_account_fixture.uuid}/{height}/"
            )

        assert serializer.data["thumbnails"] == basic_available_thumbnails

        # Premium plan - more than one thumbnail links
        serializer = ImageSerializer(image_premium_account_fixture)
        premium_available_thumbnail_heights = account_premium_fixture.plan.available_thumbnail_heights
        premium_available_thumbnails = {}
        for height in premium_available_thumbnail_heights:
            premium_available_thumbnails[f"{height}px"] = (
                settings.DEFAULT_MEDIA_DOMAIN + f"/api/v1/images/{image_premium_account_fixture.uuid}/{height}/"
            )

        assert serializer.data["thumbnails"] == premium_available_thumbnails

    def test_thumbnail_links_unauthorized(self, image_basic_account_fixture, account_basic_fixture):
        """
        Assert that Image serializer `to_representation` method does not print any thumbnail links
        and instead prints a message when there are no available thumbnails in user plan.
        """
        account_basic_fixture.plan.available_thumbnail_heights = []
        serializer = ImageSerializer(image_basic_account_fixture)

        assert serializer.data["thumbnails"] == "Thumbnails are not available for your user plan."
