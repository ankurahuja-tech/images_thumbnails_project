import magic
from django.core.exceptions import ValidationError


def validate_content_type(object):
    """
    Validates that the image is a JPEG or PNG.
    """
    valid_content_types = (
        "image/jpeg",
        "image/png",
    )
    content_type = magic.from_buffer(object.read(), mime=True)
    object.seek(0)
    
    if not content_type in valid_content_types:
        raise ValidationError("Unsupported file extension. Only PNG and JPEG files are supported.")
