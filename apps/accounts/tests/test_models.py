import pytest
from django.contrib.auth import get_user_model

from apps.plans.models import Plan

Account = get_user_model()

pytestmark = pytest.mark.django_db


class TestAccount:
    def test_create_account_and_plan_field(self):
        """
        Assert that the user is properly created, including custom `plan` field defaulting to Plan instance with id 1.
        """
        Account.objects.create_user(username="Testuser", password="testpass123")
        default_plan = Plan.objects.all().get(id=1)

        test_account = Account.objects.get(username="Testuser")

        assert Account.objects.all().count() == 1
        assert test_account.plan == default_plan
