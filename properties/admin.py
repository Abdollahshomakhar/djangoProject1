from django.contrib import admin
from .models import (
    Property,
    PropertyImage,
    PropertyFeature,
    Favorite,
    PropertyView,
)


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    fields = ("image", "alt_text", "is_main", "order")


class PropertyFeatureInline(admin.TabularInline):
    model = PropertyFeature
    extra = 1
    fields = ("name", "value")


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "property_type",
        "deal_type",
        "city",
        "area",
        "price_display",
        "status",
        "is_featured",
        "is_published",
        "created_at",
    )

    list_filter = (
        "property_type",
        "deal_type",
        "status",
        "city",
        "is_featured",
        "is_published",
        "parking",
        "elevator",
        "storage",
    )

    search_fields = (
        "title",
        "description",
        "city",
        "neighborhood",
        "address",
    )

    list_editable = (
        "status",
        "is_featured",
        "is_published",
    )

    readonly_fields = (
        "price_per_meter",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)

    inlines = (
        PropertyImageInline,
        PropertyFeatureInline,
    )

    fieldsets = (
        (
            "اطلاعات اصلی",
            {
                "fields": (
                    "title",
                    "slug",
                    "property_type",
                    "deal_type",
                    "description",
                )
            },
        ),
        (
            "مشخصات ملک",
            {
                "fields": (
                    "area",
                    "bedrooms",
                    "bathrooms",
                    "floor",
                    "total_floors",
                    "units_per_floor",
                    "year_built",
                )
            },
        ),
        (
            "قیمت",
            {
                "fields": (
                    "price",
                    "deposit",
                    "monthly_rent",
                    "price_per_meter",
                )
            },
        ),
        (
            "موقعیت",
            {
                "fields": (
                    "province",
                    "city",
                    "neighborhood",
                    "address",
                    "latitude",
                    "longitude",
                )
            },
        ),
        (
            "امکانات",
            {
                "fields": (
                    "parking",
                    "elevator",
                    "storage",
                    "balcony",
                    "furnished",
                    "air_conditioning",
                    "central_heating",
                )
            },
        ),
        (
            "وضعیت",
            {
                "fields": (
                    "status",
                    "is_featured",
                    "is_published",
                    "agent",
                )
            },
        ),
        (
            "اطلاعات سیستم",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    @admin.display(description="قیمت")
    def price_display(self, obj):
        if obj.price:
            return f"{obj.price:,.0f}"
        return "-"


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = (
        "property",
        "is_main",
        "order",
        "created_at",
    )

    list_filter = (
        "is_main",
    )

    search_fields = (
        "property__title",
    )

    list_editable = (
        "is_main",
        "order",
    )


@admin.register(PropertyFeature)
class PropertyFeatureAdmin(admin.ModelAdmin):
    list_display = (
        "property",
        "name",
        "value",
    )

    search_fields = (
        "property__title",
        "name",
        "value",
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "property",
        "created_at",
    )

    search_fields = (
        "user__username",
        "property__title",
    )

    list_filter = (
        "created_at",
    )

    readonly_fields = (
        "created_at",
    )


@admin.register(PropertyView)
class PropertyViewAdmin(admin.ModelAdmin):
    list_display = (
        "property",
        "user",
        "ip_address",
        "viewed_at",
    )

    search_fields = (
        "property__title",
        "ip_address",
        "user__username",
    )

    list_filter = (
        "viewed_at",
    )

    readonly_fields = (
        "viewed_at",
    )
