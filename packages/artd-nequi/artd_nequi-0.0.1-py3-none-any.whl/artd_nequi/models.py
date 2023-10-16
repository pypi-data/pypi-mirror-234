from django.db import models
from django.utils.translation import gettext_lazy as _
from artd_partner.models import Partner

TRANSACTION_TYPE = (
    ("PAYMENT", _("PAYMENT")),
    ("REVERSAL", _("REVERSAL")),
    ("REFUND", _("REFUND")),
    ("REVERSAL_REFUND", _("REVERSAL_REFUND")),
    ("REVERSAL_PAYMENT", _("REVERSAL_PAYMENT")),
    ("CANCEL", _("CANCEL")),
)


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        _("Created at"),
        help_text=_("Created at"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("Updated at"),
        help_text=_("Updated at"),
        auto_now=True,
    )
    status = models.BooleanField(
        _("Status"),
        help_text=_("Status"),
        default=True,
    )

    class Meta:
        abstract = True


class NequiCredential(BaseModel):
    """Model definition for Nequi Credential."""

    partner = models.OneToOneField(
        Partner,
        verbose_name=_("Partner"),
        help_text=_("Partner"),
        on_delete=models.CASCADE,
    )
    client_id = models.CharField(
        _("Client ID"),
        help_text=_("Client ID"),
        max_length=255,
    )
    client_secret = models.CharField(
        _("Client Secret"),
        help_text=_("Client Secret"),
        max_length=255,
    )
    api_key = models.CharField(
        _("API Key"),
        help_text=_("API Key"),
        max_length=255,
    )
    test_mode = models.BooleanField(
        _("Test Mode"),
        help_text=_("Test Mode"),
        default=True,
    )
    test_cellphone = models.CharField(
        _("Test Cellphone"),
        help_text=_("Test Cellphone"),
        max_length=255,
        blank=True,
        null=True,
        default="3000000000",
    )

    class Meta:
        """Meta definition for Nequi Credential."""

        verbose_name = "Nequi Credential"
        verbose_name_plural = "Nequi Credentials"

    def __str__(self):
        """Unicode representation of Nequi Credential."""
        return self.partner.name


class NequiTransaction(BaseModel):
    """Model definition for Nequi Transaction."""

    nequi_credential = models.ForeignKey(
        NequiCredential,
        verbose_name=_("Nequi Credential"),
        help_text=_("Nequi Credential"),
        on_delete=models.CASCADE,
    )
    message_id = models.CharField(
        _("Message ID"),
        help_text=_("Message ID"),
        max_length=255,
    )
    client_id = models.CharField(
        _("Client ID"),
        help_text=_("Client ID"),
        max_length=255,
    )
    value = models.CharField(
        _("Value"),
        help_text=_("Value"),
        max_length=255,
        null=True,
        blank=True,
    )
    status_code = models.CharField(
        _("Status Code"),
        help_text=_("Status Code"),
        max_length=255,
        null=True,
        blank=True,
    )
    status_description = models.CharField(
        _("Status Description"),
        help_text=_("Status Description"),
        max_length=255,
        null=True,
        blank=True,
    )
    transaction_type = models.CharField(
        _("Transaction Type"),
        help_text=_("Transaction Type"),
        max_length=255,
        choices=TRANSACTION_TYPE,
        default="PAYMENT",
    )
    transaction_id = models.CharField(
        _("Transaction ID"),
        help_text=_("Transaction ID"),
        max_length=255,
        null=True,
        blank=True,
    )
    other_data = models.JSONField(
        _("Other Data"),
        help_text=_("Other Data"),
        null=True,
        blank=True,
        default=dict,
    )

    class Meta:
        """Meta definition for Nequi Transaction."""

        verbose_name = "Nequi Transaction"
        verbose_name_plural = "Nequi Transactions"

    def __str__(self):
        """Unicode representation of Nequi Transaction."""
        return self.message_id


class NequiTransactionHisory(BaseModel):
    """Model definition for Nequi Transaction History."""

    nequi_transaction = models.ForeignKey(
        NequiTransaction,
        verbose_name=_("Nequi Transaction"),
        help_text=_("Nequi Transaction"),
        on_delete=models.CASCADE,
    )
    message_id = models.CharField(
        _("Message ID"),
        help_text=_("Message ID"),
        max_length=255,
    )
    payment_status = models.CharField(
        _("Payment Status"),
        help_text=_("Payment Status"),
        max_length=255,
        blank=True,
        null=True,
    )
    value = models.CharField(
        _("Value"),
        help_text=_("Value"),
        max_length=255,
        blank=True,
        null=True,
    )
    name = models.CharField(
        _("Name"),
        help_text=_("Name"),
        max_length=255,
        blank=True,
        null=True,
    )
    value = models.CharField(
        _("Value"),
        help_text=_("Value"),
        max_length=255,
        blank=True,
        null=True,
    )
    status_code = models.CharField(
        _("Status Code"),
        help_text=_("Status Code"),
        max_length=255,
        blank=True,
        null=True,
    )
    status_description = models.CharField(
        _("Status Description"),
        help_text=_("Status Description"),
        max_length=255,
        blank=True,
        null=True,
    )
    other_data = models.JSONField(
        _("Other Data"),
        help_text=_("Other Data"),
        null=True,
        blank=True,
        default=dict,
    )

    class Meta:
        """Meta definition for Nequi Transaction History."""

        verbose_name = "Nequi Transaction History"
        verbose_name_plural = "Nequi Transaction Histories"

    def __str__(self):
        """Unicode representation of Nequi Transaction History."""
        pass
