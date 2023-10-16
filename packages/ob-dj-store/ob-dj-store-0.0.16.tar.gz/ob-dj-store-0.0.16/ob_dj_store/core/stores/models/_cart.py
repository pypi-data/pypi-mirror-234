from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from ob_dj_store.core.stores.managers import CartItemManager, CartManager


class Cart(models.Model):
    customer = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="cart",
        primary_key=True,
    )
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CartManager()

    class Meta:
        verbose_name_plural = _("Carts")
        verbose_name = _("Cart")

    @property
    def tax_amount(self) -> Decimal:
        amount = Decimal(
            sum(map(lambda item: Decimal(item.tax_amount), self.items.all()))
        )
        return amount

    @property
    def total_price(self) -> Decimal:
        total_price = Decimal(0)
        for item in self.items.all():
            total_price += item.total_price
        return total_price

    @property
    def total_price_with_tax(self) -> Decimal:
        return self.total_price + self.tax_amount

    def __str__(self):
        return f"Cart - {self.customer.email} with total price {self.total_price}"

    def fill(self, order):
        from ob_dj_store.core.stores.models._cart import CartItem

        for item in order.items.all():
            cart_item = CartItem.objects.create(
                cart=self,
                product_variant=item.product_variant,
                store=order.store,
                notes=item.notes,
                quantity=item.quantity,
            )
            attribute_choices = list(item.attribute_choices.all())
            if len(attribute_choices) > 0:
                cart_item.attribute_choices.set(attribute_choices)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product_variant = models.ForeignKey(
        "stores.ProductVariant", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    store = models.ForeignKey(
        "stores.Store",
        on_delete=models.CASCADE,
        related_name="store_items",
        null=True,
        blank=True,
    )
    # notes for special instructions, can be empty
    notes = models.TextField(blank=True, null=True, help_text=_("Special instructions"))
    # attribute choices for the item
    attribute_choices = models.ManyToManyField(
        "stores.AttributeChoice",
        blank=True,
        related_name="cart_items",
        help_text=_("Attribute choices for the item"),
    )
    extra_infos = models.JSONField(null=True, blank=True)
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CartItemManager()

    class Meta:
        verbose_name_plural = _("Cart Items")
        verbose_name = _("Cart Item")
        ordering = [
            "created_at",
        ]

    @property
    def unit_price(self) -> Decimal:
        try:
            return self.product_variant.inventories.get(
                store=self.store
            ).discounted_price
        except ObjectDoesNotExist:
            return 0

    @property
    def tax_amount(self) -> Decimal:
        from ob_dj_store.core.stores.models import Tax

        if self.store:
            try:
                tax = Tax.objects.get(
                    country=self.store.address.country, is_active=True
                )
                if tax.rate == Tax.Rates.PERCENTAGE:
                    perc = Decimal(self.total_price * tax.value / 100)
                    return perc
                return tax.value
            except ObjectDoesNotExist:
                pass
        return 0

    @property
    def attribute_choices_total_price(self) -> Decimal:
        total_price = Decimal(0)
        for attribute_choice in self.attribute_choices.all():
            total_price += attribute_choice.price
        return total_price

    @property
    def inventory(self) -> Decimal:
        try:
            return self.product_variant.inventories.get(store=self.store)
        except ObjectDoesNotExist:
            return None

    def clean(self):
        super(CartItem, self).clean()
        if self.product_variant.product.type == "PHYSICAL" and not self.store:
            raise ValidationError(_("The store attribute can not be null"))

    @property
    def total_price(self) -> Decimal:
        return (self.unit_price + self.attribute_choices_total_price) * self.quantity

    def __str__(self):
        return f"CartItem - {self.quantity} {self.product_variant.name}"
