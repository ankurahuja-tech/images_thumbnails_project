from django.contrib import admin

from .models import Image

# Register your models here.


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """
    Base admin for Image model.
    """

    list_display = ["account", "image", "alt", "uuid", "id"]
