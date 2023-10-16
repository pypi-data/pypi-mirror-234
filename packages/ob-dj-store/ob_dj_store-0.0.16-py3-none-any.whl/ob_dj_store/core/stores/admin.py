import typing

from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from leaflet.admin import LeafletGeoAdmin

from ob_dj_store.core.stores import models
from ob_dj_store.core.stores.admin_inlines import (
    AttributeChoiceInlineAdmin,
    AvailabilityHoursInlineAdmin,
    CartItemInlineAdmin,
    InventoryInlineAdmin,
    InventoryOperationInlineAdmin,
    OpeningHoursInlineAdmin,
    OrderHistoryInlineAdmin,
    OrderItemInline,
    PhoneContactInlineAdmin,
    ProductAttributeInlineAdmin,
    ProductMediaInlineAdmin,
    ProductVariantInlineAdmin,
)


class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "shipping_fee_option",
        "shipping_fee",
        "is_active",
        "type",
    ]
    search_fields = [
        "name",
    ]
    list_filter = [
        "shipping_fee_option",
        "is_active",
        "type",
    ]


class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "payment_provider",
        "is_active",
    ]
    search_fields = [
        "name",
    ]
    list_filter = ["payment_provider", "is_active"]


class StoreAdmin(LeafletGeoAdmin):
    inlines = [PhoneContactInlineAdmin, OpeningHoursInlineAdmin, InventoryInlineAdmin]
    list_display = [
        "name",
        "location",
        "is_active",
        "busy_mode",
        "currency",
        "minimum_order_amount",
        "delivery_charges",
        "min_free_delivery_amount",
    ]
    # define the pickup addresses field as a ManyToManyField
    # to the address model
    filter_horizontal = ["pickup_addresses"]
    # define the shipping methods field as a ManyToManyField
    # to the shipping method model
    filter_horizontal = ["shipping_methods"]
    search_fields = ["name", "address__address_line"]
    list_filter = ("is_active",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "location",
                    "address",
                    "is_active",
                    "poly",
                    "minimum_order_amount",
                    "payment_methods",
                    "pickup_addresses",
                    "image",
                    "currency",
                )
            },
        ),
        (
            "shipping info",
            {
                "fields": (
                    "shipping_methods",
                    "delivery_charges",
                    "min_free_delivery_amount",
                )
            },
        ),
    )


class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        AvailabilityHoursInlineAdmin,
    ]
    list_display = ["name", "is_active", "parent", "image"]
    search_fields = [
        "name",
    ]
    list_filter = [
        "is_active",
    ]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .prefetch_related(
                "availability_hours",
            )
        )


class ProductVariantAdmin(admin.ModelAdmin):
    inlines = [
        InventoryInlineAdmin,
        ProductAttributeInlineAdmin,
    ]
    list_display = [
        "name",
        "label",
        "product",
        "is_special",
        "has_inventory",
    ]
    search_fields = ["name", "product__name", "sku"]
    exclude = ("product_attributes",)

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("product")
            .prefetch_related(
                "inventories",
                "inventories__store",
                "product_attributes",
                "product_attributes__attribute_choices",
            )
        )


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = "__all__"

    def clean_category(self):
        categories = self.cleaned_data.get("category")
        for category in categories:
            if not category.parent:
                raise forms.ValidationError(_("Category Doesn't have a parent"))
        return categories


class MenuAdmin(admin.ModelAdmin):
    list_display = ["id", "store", "name", "created_at"]
    search_fields = [
        "store",
    ]


class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "categories", "type", "is_active"]
    form = ProductAdminForm

    inlines = [
        ProductVariantInlineAdmin,
        ProductMediaInlineAdmin,
    ]
    list_filter = ["type", "is_active"]
    search_fields = ["name", "category__name"]

    def categories(self, obj):
        return [category.name for category in obj.category.all()]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .prefetch_related(
                "category",
            )
        )


class ProductAttributeAdmin(admin.ModelAdmin):
    inlines = [
        AttributeChoiceInlineAdmin,
    ]
    list_display = ["id", "name", "type", "is_mandatory"]
    search_fields = [
        "name",
    ]
    list_filter = ["is_mandatory", "type"]
    exclude = ("attribute_choices",)


class AttributeChoiceAdmin(admin.ModelAdmin):
    list_display = ["name", "price"]
    search_fields = [
        "name",
    ]


class ProductTagAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = [
        "name",
    ]

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.base_fields["text_color"].widget = forms.TextInput(attrs={"type": "color"})
        form.base_fields["background_color"].widget = forms.TextInput(
            attrs={"type": "color"}
        )
        return form


class CartAdmin(admin.ModelAdmin):
    list_display = ["customer", "total_price"]
    inlines = [CartItemInlineAdmin]
    search_fields = [
        "customer__email",
    ]


class AdressAdmin(LeafletGeoAdmin):
    list_display = [
        "id",
        "address_line",
        "postal_code",
        "city",
        "region",
        "country",
        "is_active",
    ]
    search_fields = [
        "address_line",
        "city",
        "region",
        "country",
    ]
    list_filter = [
        "is_active",
    ]


class OrderAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = [
        "id",
        "customer",
        "status",
        "type_of_order",
        "payment_method",
        "store",
        "total_amount",
        "pickup_time",
        "created_at",
    ]
    inlines = [OrderItemInline, OrderHistoryInlineAdmin]
    search_fields = [
        "customer__email",
    ]
    date_hierarchy = "created_at"
    list_filter = [
        "payment_method",
        "shipping_method",
        "store",
        "status",
    ]

    def get_queryset(self, request):
        queryset = (
            super()
            .get_queryset(request)
            .select_related(
                "shipping_method",
                "payment_method",
                "store",
                "customer",
            )
            .prefetch_related(
                "items",
                "items__product_variant__inventories",
                "items__attribute_choices",
            )
        )
        return queryset


class PaymentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "method",
        "amount",
        "currency",
        "status",
        "payment_post_at",
        "created_at",
    )
    list_filter = [
        "method__payment_provider",
        "status",
    ]
    search_fields = ["orders__store__name", "user__email"]
    readonly_fields = ("orders",)
    date_hierarchy = "created_at"


class InventoryAdmin(admin.ModelAdmin):
    inlines = [InventoryOperationInlineAdmin]
    list_display = [
        "variant",
        "store",
        "quantity",
        "is_snoozed",
        "is_active",
        "price",
        "discount_percent",
        "is_uncountable",
        "preparation_time",
    ]
    list_filter = [
        "is_deliverable",
        "is_primary",
        "is_uncountable",
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("store")


class TaxAdmin(admin.ModelAdmin):
    list_display = [
        "value",
        "name",
        "rate",
        "is_applied",
        "country",
        "value",
        "is_active",
    ]
    list_filter = [
        "is_applied",
        "is_active",
        "rate",
    ]


class WalletTransactionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "type",
        "amount",
        "is_cashback",
        "is_refund",
        "created_at",
    ]
    list_filter = [
        "type",
    ]
    search_fields = [
        "wallet__user__email",
    ]

    def user(self, obj) -> typing.Text:
        return obj.wallet.user.email


class WalletAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "balance", "currency")
    search_fields = [
        "user__email",
    ]


class WalletMediaAdmin(admin.ModelAdmin):
    list_display = ("id", "image", "image_thumbnail_medium", "is_active")


class AvailabilityHoursAdmin(admin.ModelAdmin):
    list_display = ("id", "store", "category", "from_hour", "to_hour")


admin.site.register(models.Store, StoreAdmin)
admin.site.register(models.ShippingMethod, ShippingMethodAdmin)
admin.site.register(models.PaymentMethod, PaymentMethodAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductAttribute, ProductAttributeAdmin)
admin.site.register(models.ProductVariant, ProductVariantAdmin)
# admin.site.register(models.ProductTag, ProductTagAdmin)
admin.site.register(models.Cart, CartAdmin)
admin.site.register(models.Address, AdressAdmin)
admin.site.register(models.AttributeChoice, AttributeChoiceAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Payment, PaymentAdmin)
admin.site.register(models.Inventory, InventoryAdmin)
admin.site.register(models.Tax, TaxAdmin)
admin.site.register(models.WalletTransaction, WalletTransactionAdmin)
admin.site.register(models.Wallet, WalletAdmin)
admin.site.register(models.WalletMedia, WalletMediaAdmin)
admin.site.register(models.AvailabilityHours, AvailabilityHoursAdmin)
admin.site.register(models.Menu, MenuAdmin)
