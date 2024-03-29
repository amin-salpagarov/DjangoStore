from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("__str__", "status")
    fields = (
        "id",
        (
            "first_name",
            "last_name",
        ),
        "email",
        "address",
        "created",
        "status",
        "initiator",
        "basket_history",
    )
    readonly_fields = ("created", "id")
