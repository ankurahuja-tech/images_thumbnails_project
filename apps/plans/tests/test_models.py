import pytest

from apps.plans.models import Plan

pytestmark = pytest.mark.django_db


class TestImage:
    def test_default_plans_exist(self):
        """
        Assert that the default Plan instances were created.
        """
        plans = Plan.objects.all()
        assert plans.count() == 3
        assert plans[0].name == "Basic"
        assert plans[1].name == "Premium"
        assert plans[2].name == "Enterprise"

    def test_create_plan(self):
        """
        Assert that the custom plan is properly created.
        """
        Plan.objects.create(
            name="Custom",
            available_thumbnail_heights=[100, 200, 300, 400, 500, 600],
            can_access_original_image=True,
            can_fetch_expiring_link=True,
            expiring_link_time_range=(100, 200),
        )
        test_plan = Plan.objects.get(name="Custom")

        assert Plan.objects.all().count() == 4
        assert test_plan.available_thumbnail_heights == [100, 200, 300, 400, 500, 600]
