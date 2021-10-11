import io
import json
import time

import PIL
import pytest
from django.conf import settings
from django.urls import resolve, reverse
from psycopg2.extras import NumericRange

from apps.images.api.views import (
    ImageExpiringLinkAPIView,
    ImageGenerateLinkAPIView,
    ThumbnailRenderAPIView,
)
from apps.images.api.viewsets import ImageViewSet
from apps.images.models import Image
from apps.plans.models import Plan


class TestImageViewsets:
    def test_list(self, api_client, account_premium_fixture, image_premium_account_fixture):
        """
        Assert that Image viewset correctly lists (GET) Image data.
        """
        response = api_client.get(reverse("apiv1:images-list"))
        response_content = json.loads(response.content)

        assert response.status_code == 200
        assert len(response_content) == 1
        assert response_content[0]["id"] == image_premium_account_fixture.id

    def test_list_url_resolves_image_view_set(self, api_client):
        """
        Assert that the expected url resolves correct view set.
        """
        url = reverse("apiv1:images-list")
        view = resolve(url)
        assert view.func.__name__ == ImageViewSet.as_view({"get": "list"}).__name__

    def test_retrieve(self, api_client, account_premium_fixture, image_premium_account_fixture):
        """
        Assert that Image viewset correctly details (GET) Image data.
        """
        response = api_client.get(reverse("apiv1:images-detail", kwargs={"uuid": image_premium_account_fixture.uuid}))
        response_content = json.loads(response.content)

        assert response.status_code == 200
        assert (
            len(response_content) == 6
        )  # 5 base Image serializer fields + `thumbnails` field added from `to representation` Image method
        assert response_content["thumbnails"]
        assert response_content["id"] == image_premium_account_fixture.id

    def test_retrieve_url_resolves_image_view_set(
        self, api_client, account_premium_fixture, image_premium_account_fixture
    ):
        """
        Assert that the expected url resolves correct view set.
        """
        url = reverse("apiv1:images-detail", kwargs={"uuid": image_premium_account_fixture.uuid})
        view = resolve(url)

        assert view.func.__name__ == ImageViewSet.as_view({"get": "detail"}).__name__

    def test_create(self, api_client, image_serializer_valid_data_fixture):
        """
        Assert that Image viewset correctly posts (POST) Image data.
        """
        post = image_serializer_valid_data_fixture
        response = api_client.post(reverse("apiv1:images-list"), post)
        data = json.loads(response.content)

        assert response.status_code == 201
        print(data)
        print(type(data))
        assert data["account"] == image_serializer_valid_data_fixture["account"]

    def test_update(self, api_client, account_premium_fixture, image_premium_account_fixture):
        """
        Assert that Image viewset correctly updates (PUT) Image data.
        """
        put = {
            "id": image_premium_account_fixture.id,
            "account": image_premium_account_fixture.account.id,
            "image": image_premium_account_fixture.image,
            "uuid": image_premium_account_fixture.uuid,
            "alt": "updated alt field",
            "created_at": image_premium_account_fixture.created_at,
            "modified_at": image_premium_account_fixture.modified_at,
        }
        response = api_client.put(
            reverse("apiv1:images-detail", kwargs={"uuid": image_premium_account_fixture.uuid}), put
        )
        data = json.loads(response.content)

        assert response.status_code == 200
        assert data["account"] == image_premium_account_fixture.account.id
        assert data["alt"] == put["alt"]

    def test_delete(self, api_client, image_premium_account_fixture):
        """
        Assert that Image viewset correctly deletes (DELETE) Image data.
        """
        response = api_client.delete(
            reverse("apiv1:images-detail", kwargs={"uuid": image_premium_account_fixture.uuid})
        )

        assert response.status_code == 204
        assert Image.objects.all().count() == 0


class TestThumbnailAPIViews:
    def test_retrieve_render_height_available(self, api_client, image_premium_account_fixture):
        """
        Assert that Image thumbnail view correctly renders thumbnail when given height available
        to the Image owner's plan.
        """
        available_height = image_premium_account_fixture.account.plan.available_thumbnail_heights[0]
        response = api_client.get(
            reverse(
                "apiv1:images_render_thumbnail",
                kwargs={"uuid": image_premium_account_fixture.uuid, "height": available_height},
            )
        )
        rendered_image = PIL.Image.open(io.BytesIO(response.content))

        assert response.status_code == 200
        assert rendered_image.format == "JPEG"
        assert rendered_image.height == available_height

    def test_retrieve_render_height_unavailable(self, api_client, image_premium_account_fixture):
        """
        Assert that Image thumbnail view raises 403 Forbidden error when given height unavailable
        to the Image owner's plan.
        """
        unavailable_height = image_premium_account_fixture.account.plan.available_thumbnail_heights[0] + 10
        response = api_client.get(
            reverse(
                "apiv1:images_render_thumbnail",
                kwargs={"uuid": image_premium_account_fixture.uuid, "height": unavailable_height},
            )
        )

        assert response.status_code == 403

    def test_retrieve_render_wrong_user(self, api_client, image_premium_account_fixture, account_basic_fixture):
        """
        Assert that Image thumbnail view raises 403 Forbidden error when requesting user is not the owner of the Image.
        """
        available_height = account_basic_fixture.plan.available_thumbnail_heights[0]
        response = api_client.get(
            reverse(
                "apiv1:images_render_thumbnail",
                kwargs={"uuid": image_premium_account_fixture.uuid, "height": available_height},
            )
        )

        assert response.status_code == 403

    def test_retrieve_render_url_resolves_thumbnail_retrieve_api_view(
        self, api_client, account_premium_fixture, image_premium_account_fixture
    ):
        """
        Assert that the expected url resolves correct view.
        """
        url = reverse(
            "apiv1:images_render_thumbnail",
            kwargs={
                "uuid": image_premium_account_fixture.uuid,
                "height": account_premium_fixture.plan.available_thumbnail_heights[0],
            },
        )
        view = resolve(url)
        assert view.func.__name__ == ThumbnailRenderAPIView.as_view().__name__


class TestImageGenerateLinkAPIViews:
    def test_retrieve_generate_link_available(
        self, api_client, account_enterprise_fixture, image_enterprise_account_fixture
    ):
        """
        Assert that the view correctly generates valid expiring link when entered by a user
        whose plan authorizes to generate expiring links within given time bounds.
        """
        uuid = image_enterprise_account_fixture.uuid
        valid_expiry_time = 450
        query_string_start = "?sesame"
        response = api_client.get(
            reverse("apiv1:images_generate_link", kwargs={"uuid": uuid, "expiry_time": valid_expiry_time})
        )
        response_content = json.loads(response.content)

        expiring_link = (
            settings.DEFAULT_MEDIA_DOMAIN + f"/api/v1/images/{uuid}/link/{valid_expiry_time}/" + query_string_start
        )

        assert response.status_code == 200
        assert len(response_content) == 2
        assert response_content["Time to expire"] == f"{valid_expiry_time} seconds"
        assert response_content["Expiring link"].startswith(expiring_link)

    def test_retrieve_generate_link_unavailable(
        self, api_client, account_premium_fixture, image_premium_account_fixture
    ):
        """
        Assert that the view does not generate an expiring link when entered by a user
        whose plan does not authorize to generate expiring links.
        """
        uuid = image_premium_account_fixture.uuid
        expiry_time = 450
        response = api_client.get(
            reverse("apiv1:images_generate_link", kwargs={"uuid": uuid, "expiry_time": expiry_time})
        )
        response_content = json.loads(response.content)

        assert response.status_code == 403
        assert len(response_content) == 1

    def test_retrieve_generate_link_out_of_bounds(
        self, api_client, account_enterprise_fixture, image_enterprise_account_fixture
    ):
        """
        Assert that the view does not generate an expiring link when entered by a user
        whose plan authorizes to generate expiring links, but when given invalid time bounds.
        """
        uuid = image_enterprise_account_fixture.uuid
        invalid_expiry_time = 299
        response = api_client.get(
            reverse("apiv1:images_generate_link", kwargs={"uuid": uuid, "expiry_time": invalid_expiry_time})
        )
        response_content = json.loads(response.content)

        assert response.status_code == 403
        assert len(response_content) == 1

    def test_retrieve_generate_link_url_resolves_image_generate_link_retrieve_api_view(
        self, api_client, image_enterprise_account_fixture
    ):
        """
        Assert that the expected url resolves correct view.
        """
        uuid = image_enterprise_account_fixture.uuid
        expiry_time = 450
        url = reverse("apiv1:images_generate_link", kwargs={"uuid": uuid, "expiry_time": expiry_time})
        view = resolve(url)

        assert view.func.__name__ == ImageGenerateLinkAPIView.as_view().__name__


class TestImageExpiringLinkAPIViews:
    def test_retrieve_expiring_link_valid(self, api_client, image_enterprise_account_fixture):
        """
        Assert that the view correctly renders image for an unauthenticated user when provided
        with expiring link properly generated by the authenticated, authorized user.
        """
        # Generate valid expiring link and logout the user
        uuid = image_enterprise_account_fixture.uuid
        valid_expiry_time = 450
        response = api_client.get(
            reverse("apiv1:images_generate_link", kwargs={"uuid": uuid, "expiry_time": valid_expiry_time})
        )
        generate_link_content = json.loads(response.content)
        expiring_link = generate_link_content["Expiring link"]
        api_client.logout()

        # Retrieve expiring link
        response = api_client.get(expiring_link)
        rendered_image = PIL.Image.open(io.BytesIO(response.content))

        assert response.status_code == 200
        assert rendered_image.format == "JPEG"

    def test_retrieve_expiring_link_expired(self, api_client, image_enterprise_account_fixture):
        """
        Assert that the view does not render the image when provided with an expired link.
        """
        # Update Enterprise plan to shorten the minimum valid time of the expiring link
        Plan.objects.filter(name=image_enterprise_account_fixture.account.plan).update(
            expiring_link_time_range=NumericRange(lower=1, upper=2)
        )
        image_enterprise_account_fixture.account.refresh_from_db()

        # Generate valid expiring link
        uuid = image_enterprise_account_fixture.uuid
        valid_expiry_time = 1
        response = api_client.get(
            reverse("apiv1:images_generate_link", kwargs={"uuid": uuid, "expiry_time": valid_expiry_time})
        )
        generate_link_content = json.loads(response.content)
        expiring_link = generate_link_content["Expiring link"]

        # Wait through expiry time and retrieve expiring link
        time.sleep(valid_expiry_time)
        response = api_client.get(expiring_link)

        assert response.status_code == 403

    def test_retrieve_generate_link_url_resolves_image_generate_link_retrieve_api_view(
        self, api_client, image_enterprise_account_fixture
    ):
        """
        Assert that the expected url resolves correct view.
        """
        uuid = image_enterprise_account_fixture.uuid
        expiry_time = 450
        url = reverse("apiv1:images_expiring_link", kwargs={"uuid": uuid, "expiry_time": expiry_time})
        view = resolve(url)

        assert view.func.__name__ == ImageExpiringLinkAPIView.as_view().__name__
