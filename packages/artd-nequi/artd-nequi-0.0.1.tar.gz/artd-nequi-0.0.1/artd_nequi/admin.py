from django.contrib import admin
from artd_nequi.models import NequiCredential, NequiTransaction, NequiTransactionHisory
from django_json_widget.widgets import JSONEditorWidget
from django.db import models


@admin.register(NequiCredential)
class NequiCredentialAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "partner",
        "client_id",
        "client_secret",
        "api_key",
        "status",
    )
    list_filter = ("status",)
    search_fields = (
        "partner__name",
        "client_id",
        "client_secret",
        "api_key",
    )
    ordering = (
        "partner",
        "client_id",
        "client_secret",
        "api_key",
        "status",
    )


@admin.register(NequiTransaction)
class NequiTransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "status",
        "nequi_credential",
        "transaction_type",
        "message_id",
    )
    list_filter = (
        "status",
        "transaction_type",
    )
    search_fields = (
        "nequi_credential__partner__name",
        "message_id",
        "transaction_type",
    )
    ordering = [
        "-id",
    ]
    formfield_overrides = {
        models.JSONField: {
            "widget": JSONEditorWidget,
        },
    }


@admin.register(NequiTransactionHisory)
class NequiTransactionHisoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nequi_transaction",
        "message_id",
        "status_code",
        "status_description",
        "value",
    )
    list_filter = (
        "status_code",
        "status_description",
    )
    search_fields = (
        "nequi_transaction__nequi_credential__partner__name",
        "message_id",
        "status_code",
        "status_description",
        "value",
    )
    ordering = [
        "-id",
    ]
    formfield_overrides = {
        models.JSONField: {
            "widget": JSONEditorWidget,
        },
    }
