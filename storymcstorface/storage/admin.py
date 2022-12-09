from django.contrib import admin
from storage.models import (
    Location,
    Facility,
    StorageItem,
    Product,
    ProductCategory,
    StorageLog,
    Vendor,
)


class ProductInline(admin.TabularInline):
    model = Product
    exclude = ("slug",)


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    inlines = [ProductInline]


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    pass


class LocationInline(admin.TabularInline):
    model = Location
    ordering = ("row", "column")


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    inlines = [LocationInline]
    exclude = ("slug",)


@admin.register(StorageItem)
class StorageItemAdmin(admin.ModelAdmin):
    list_display = ("product", "location")
    list_filter = ("location__facility",)


@admin.register(StorageLog)
class StorageLogAdmin(admin.ModelAdmin):
    list_display = (
        "timestamp",
        "user",
        "action",
        "quantity",
        "get_facility",
        "get_location",
        "item",
    )
    list_filter = ("user", "item", "action", "timestamp")
