import os

from django.conf import settings
from django.core.files.storage import default_storage
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from sesame.utils import get_query_string, get_user

from ..models import Image
from .permissions import IsOwner
from .renderers import JPEGRenderer, PNGRenderer
from .utils import create_thumbnail


class ThumbnailRenderAPIView(RetrieveAPIView):
    """
    Base detail view for viewing a rendered thumbnail.
    Output in JPEG format.
    """

    permission_classes = (IsAuthenticated, IsOwner)
    renderer_classes = [JPEGRenderer]

    def get(self, request, *args, **kwargs):
        """
        Checks if the user has permission to generate and view thumbnails of requested height:
        - if yes, checks if such thumbnail exists at MEDIA ROOT (if not, generates and saves it)
        and returns it in JPEG format,
        - if not, raises PermissionDenied error.
        """
        request_height = self.kwargs["height"]
        request_uuid = self.kwargs["uuid"]
        available_heights = request.user.plan.available_thumbnail_heights

        # Checks if the requested height is available and if yes, returns a response with the thumbnail
        if request_height in available_heights:
            thumbnail_file_path = os.path.join(
                settings.MEDIA_ROOT, f"images/{request.user}/{request_uuid}/{request_height}-{request_uuid}.jpg"
            )

            # Checks if the thumbnail file exists and if not, creates it
            thumbnail_exists = default_storage.exists(thumbnail_file_path)
            if not thumbnail_exists:
                source_image = Image.objects.get(uuid=self.kwargs["uuid"])
                if source_image.account == request.user:
                    source_image_file = source_image.image
                    create_thumbnail(image_file=source_image_file, height=request_height, path=thumbnail_file_path)
                else:
                    raise PermissionDenied("You are not authorized to view this thumbnail.")

            # Returns the rendered thumbnail
            with open(thumbnail_file_path, "rb") as thumbnail:
                data = thumbnail.read()
                return Response(data, content_type="image/jpeg")

        else:
            raise PermissionDenied(
                f"Requested thumbnail height is not available for your user plan. "
                f"Supported heights (px): {available_heights}."
            )


class ImageGenerateLinkAPIView(RetrieveAPIView):
    """
    Base view for generating an expiring link to the image.
    """

    permission_classes = (IsAuthenticated, IsOwner)

    def get(self, request, *args, **kwargs):
        """
        Checks if the user is authorized to generate expiring links and if the provided expiry time value
        is within bounds of the requesting user's account plan.
        If yes, generates a unique, expiring link to the image with the given expiry time. Else, raises error.
        """
        uuid = self.kwargs["uuid"]
        expiry_time = self.kwargs["expiry_time"]

        expiry_time_bounds = request.user.plan.expiring_link_time_range
        if request.user.plan.can_fetch_expiring_link:
            if (not expiry_time_bounds.lower or expiry_time_bounds.lower <= expiry_time) and (
                not expiry_time_bounds.upper or expiry_time_bounds.upper >= expiry_time
            ):
                unique_query_string = get_query_string(request.user)
                expiring_link = (
                    settings.DEFAULT_MEDIA_DOMAIN + f"/api/v1/images/{uuid}/link/{expiry_time}/" + unique_query_string
                )

                content = {
                    "Expiring link": expiring_link,
                    "Time to expire": str(expiry_time) + " seconds",
                }
                return Response(content)

            else:
                raise PermissionDenied(
                    f"Invalid expiry time given. Valid expiry time is between {expiry_time_bounds.lower} "
                    f"seconds and {expiry_time_bounds.upper} seconds."
                )
        else:
            raise PermissionDenied("You are not authorized to generate expiring links.")


class ImageExpiringLinkAPIView(RetrieveAPIView):
    """
    Base view for displaying an image, provided a valid expiring link was given.
    """

    permission_classes = (AllowAny,)
    renderer_classes = [JPEGRenderer, PNGRenderer]

    def get(self, request, *args, **kwargs):
        """
        Checks if the provided link is valid and has not yet expired.
        If the link is valid, renders the desired image.
        """
        user = get_user(request, max_age=self.kwargs["expiry_time"])
        if user is None:
            raise PermissionDenied("This link is not valid or has expired.")

        else:
            queryset = Image.objects.get(uuid=self.kwargs["uuid"]).image
            data = queryset

            image_name = data.name
            if image_name.endswith(".png"):
                content_type = "image/png"
            else:
                content_type = "image/jpeg"

            return Response(data, content_type=content_type)
