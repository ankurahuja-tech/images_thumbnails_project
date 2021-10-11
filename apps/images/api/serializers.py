from django.conf import settings
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from ..models import Image


class ImageSerializer(serializers.ModelSerializer):
    """
    Serializer for Image model.
    """

    class Meta:
        model = Image
        fields = ["id", "account", "image", "alt", "uuid"]

    def validate_image(self, value):
        """
        Validates that the image field contains a file with PNG or JPEG extension.
        """
        valid_extensions = [".png", ".jpg", ".jpeg"]
        image_filename = value.name.lower()
        for extension in valid_extensions:
            if image_filename.endswith(extension):
                return value
        else:
            raise ValidationError("Unsupported file extension. Only PNG and JPEG files are supported.")

    def to_representation(self, instance):
        """
        Adds `thumbnails` field to json response and checks if the requesting user's plan:
        - authorizes to access original image; if yes, returns a link for the original image,
        - provides possible thumbnail heights; if yes, returns links to thumbnails of given heights.
        """
        representation = super().to_representation(instance)

        # Check if the user can access original image and if no, hides its link
        plan = instance.account.plan
        if not plan.can_access_original_image:
            representation["image"] = "Original image is not available for your user plan."

        # Check if the user can access thumbnails and if yes, provides links to them
        available_heights = plan.available_thumbnail_heights
        if available_heights:
            representation["thumbnails"] = {}
            for height in plan.available_thumbnail_heights:
                representation["thumbnails"][f"{height}px"] = (
                    settings.DEFAULT_MEDIA_DOMAIN + f"/api/v1/images/{instance.uuid}/{height}/"
                )
        else:
            representation["thumbnails"] = "Thumbnails are not available for your user plan."

        return representation
