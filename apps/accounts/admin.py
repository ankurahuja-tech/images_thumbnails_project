from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

# Register your models here.

Account = get_user_model()


@admin.register(Account)
class AccountAdmin(UserAdmin):
    """
    Base admin for user Account model.
    """

    model = Account
    list_display = [
        "username",
        "email",
        "is_staff",
        "is_superuser",
        "is_active",
        "plan",
    ]

    fieldsets = (
        (None, {"fields": ("username", "password", "plan")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "plan"),
            },
        ),
    )
