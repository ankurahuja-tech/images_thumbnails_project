import datetime
import os
import shutil
import tempfile
import uuid as uuid_lib

import pytest
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework.test import APIClient

from apps.images.models import Image
from apps.plans.models import Plan
from config.settings.base import AUTH_USER_MODEL

MEDIA_ROOT_TEST = tempfile.mkdtemp()
IMAGE_FILE_JPEG_TEST = open(os.path.join(settings.BASE_DIR, "test_media_files/test_image.jpg"), "rb").read()
IMAGE_FILE_GIF_TEST = open(os.path.join(settings.BASE_DIR, "test_media_files/test_image.gif"), "rb").read()


@pytest.fixture
def api_client():
    return APIClient()


# Account fixtures


@pytest.fixture
def account_basic_fixture(db, django_user_model: AUTH_USER_MODEL, api_client: APIClient) -> AUTH_USER_MODEL:
    """
    Creates and authenticates a user with the Basic plan.
    """
    account_basic = django_user_model.objects.create_user(username="account_basic", password="testpass123")
    api_client.force_authenticate(user=account_basic)
    return account_basic


@pytest.fixture
def account_premium_fixture(db, django_user_model: AUTH_USER_MODEL, api_client: APIClient) -> AUTH_USER_MODEL:
    """
    Creates and authenticates a user with the Premium plan.
    """
    premium = Plan.objects.get(id=2)
    account_premium = django_user_model.objects.create_user(
        username="account_premium", password="testpass123", plan=premium
    )
    api_client.force_authenticate(user=account_premium)
    return account_premium


@pytest.fixture
def account_enterprise_fixture(db, django_user_model: AUTH_USER_MODEL, api_client: APIClient) -> AUTH_USER_MODEL:
    """
    Creates and authenticates a user with the Enterprise plan.
    """
    enterprise = Plan.objects.get(id=3)
    account_enterprise = django_user_model.objects.create_user(
        username="account_enterprise", password="testpass123", plan=enterprise
    )
    api_client.force_authenticate(user=account_enterprise)
    return account_enterprise


# Image fixtures


@override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
@pytest.fixture
def image_basic_account_fixture(account_basic_fixture: AUTH_USER_MODEL, request) -> Image:
    """
    Creates Image instance for a user with a Basic account and creates image file in `media` folder.
    After the tests are run, deletes the temp folder.
    """
    image = Image.objects.create(
        account=account_basic_fixture,
        image=SimpleUploadedFile(name="image.jpg", content=IMAGE_FILE_JPEG_TEST, content_type="image/jpeg"),
        alt="Image fixture",
        uuid=uuid_lib.uuid4(),
        created_at=datetime.datetime.now(),
        modified_at=datetime.datetime.now(),
    )

    def delete_image_folder():
        folder_path = os.path.join(settings.MEDIA_ROOT, f"images/{account_basic_fixture}/")
        shutil.rmtree(folder_path)

    request.addfinalizer(delete_image_folder)
    return image


@override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
@pytest.fixture
def image_premium_account_fixture(account_premium_fixture: AUTH_USER_MODEL, request) -> Image:
    """
    Creates Image instance for a user with Premium account and creates image file in `media` folder.
    After the tests are run, deletes the temp folder.
    """
    image = Image.objects.create(
        account=account_premium_fixture,
        image=SimpleUploadedFile(name="image.jpg", content=IMAGE_FILE_JPEG_TEST, content_type="image/jpeg"),
        alt="Image fixture",
        uuid=uuid_lib.uuid4(),
        created_at=datetime.datetime.now(),
        modified_at=datetime.datetime.now(),
    )

    def delete_image_folder():
        folder_path = os.path.join(settings.MEDIA_ROOT, f"images/{account_premium_fixture}/")
        shutil.rmtree(folder_path)

    request.addfinalizer(delete_image_folder)
    return image


@override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
@pytest.fixture
def image_enterprise_account_fixture(account_enterprise_fixture: AUTH_USER_MODEL, request) -> Image:
    """
    Creates Image instance for a user with Enterprise account and creates image file in `media` folder.
    After the tests are run, deletes the temp folder.
    """
    image = Image.objects.create(
        account=account_enterprise_fixture,
        image=SimpleUploadedFile(name="image.jpg", content=IMAGE_FILE_JPEG_TEST, content_type="image/jpeg"),
        alt="Image fixture",
        uuid=uuid_lib.uuid4(),
        created_at=datetime.datetime.now(),
        modified_at=datetime.datetime.now(),
    )

    def delete_image_folder():
        folder_path = os.path.join(settings.MEDIA_ROOT, f"images/{account_enterprise_fixture}/")
        shutil.rmtree(folder_path)

    request.addfinalizer(delete_image_folder)
    return image


@override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
@pytest.fixture
def image_serializer_valid_data_fixture(account_premium_fixture: AUTH_USER_MODEL) -> dict:
    """
    Valid data for Image serializer.
    Includes valid image file extension, i.e. JPG.
    """
    image_serializer_data = {
        "account": account_premium_fixture.id,
        "image": SimpleUploadedFile(
            name="test_image.jpg",
            content=IMAGE_FILE_JPEG_TEST,
            content_type="image/jpeg",
        ),
        "alt": "Image fixture",
        "uuid": uuid_lib.uuid4(),
        "created_at": datetime.datetime.now(),
        "modified_at": datetime.datetime.now(),
    }
    return image_serializer_data


@override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
@pytest.fixture
def image_serializer_invalid_data_fixture(account_premium_fixture: AUTH_USER_MODEL) -> dict:
    """
    Invalid data for Image serializer.
    Includes invalid image file extension, i.e. GIF.
    """
    image_serializer_data = {
        "account": account_premium_fixture.id,
        "image": SimpleUploadedFile(
            name="test_image.gif",
            content=IMAGE_FILE_GIF_TEST,
            content_type="image/gif",
        ),
        "alt": "Image fixture",
        "uuid": uuid_lib.uuid4(),
        "created_at": datetime.datetime.now(),
        "modified_at": datetime.datetime.now(),
    }
    return image_serializer_data
