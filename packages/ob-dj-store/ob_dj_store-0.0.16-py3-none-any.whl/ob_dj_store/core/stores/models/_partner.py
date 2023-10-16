import logging
from datetime import timedelta

from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from ob_dj_otp.core.otp.models import OneTruePairing

from ob_dj_store.core.stores.managers import PartnerAuthInfoManager
from ob_dj_store.utils.model import DjangoModelCleanMixin

logger = logging.getLogger(__name__)


class Discount(models.Model):
    discount_rate = models.DecimalField(
        max_digits=3, decimal_places=2, validators=[MaxValueValidator(limit_value=1)]
    )
    is_active = models.BooleanField(default=True)

    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Discount(PK={self.pk})"

    def perc_to_flat(self, amount):
        return amount * self.discount_rate


class Partner(DjangoModelCleanMixin, models.Model):
    class AuthMethods(models.TextChoices):
        OTP = "OTP", _("One True Pairing")
        CODE = "CODE", _("Promotion code")

    name = models.CharField(_("Partner's Name"), max_length=255)
    promotion_code = models.PositiveBigIntegerField(
        _("Promotion code"), null=True, blank=True
    )
    auth_method = models.CharField(
        _("Authentication method"), max_length=255, choices=AuthMethods.choices
    )
    country = CountryField(help_text=_("Partner's country."))
    discount = models.ForeignKey(
        Discount, on_delete=models.PROTECT, related_name="partners"
    )

    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name}"


class PartnerEmailDomain(DjangoModelCleanMixin, models.Model):
    partner = models.ForeignKey(
        Partner, on_delete=models.CASCADE, related_name="domains"
    )
    email_domain = models.CharField(max_length=255)

    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PartnerAuthInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField(_("Partner's Email"))
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    authentication_details = models.JSONField(null=True, blank=True)
    authentication_expires = models.DateTimeField()

    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(_("Last Authentifacation"), auto_now=True)

    objects = PartnerAuthInfoManager()

    def save(self, **kwargs) -> None:
        self.authentication_expires = now() + timedelta(
            days=getattr(settings, "PARTNER_AUTH_TIME", 365)
        )
        return super().save(**kwargs)


class PartnerOTPAuth(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    otp = models.OneToOneField(
        OneTruePairing, on_delete=models.PROTECT, related_name="partner_otp_auth"
    )
    partner = models.ForeignKey(
        Partner, on_delete=models.CASCADE, related_name="otp_auths"
    )
    email = models.EmailField(_("Partner's Email"))

    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"PartnerOTPAuth(PK={self.pk})"
