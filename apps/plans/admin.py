from django.contrib import admin

from .models import Plan

# Register your models here.


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    """
    Base admin for Plan model.
    """

    model = Plan
    list_display = [
        "name",
        "available_thumbnail_heights",
        "can_access_original_image",
        "can_fetch_expiring_link",
        "expiring_link_time_range",
    ]
