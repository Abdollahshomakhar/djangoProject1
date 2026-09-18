from django.db import models
from django.contrib.auth.models import User

from django.utils.text import slugify


class Property(models.Model):
    class PropertyType(models.TextChoices):
        APARTMENT = "apartment", "آپارتمان"
        VILLA = "villa", "ویلا"
        HOUSE = "house", "خانه"
        LAND = "land", "زمین"
        OFFICE = "office", "دفتر کار"
        SHOP = "shop", "مغازه"
        COMMERCIAL = "commercial", "ملک تجاری"
        WAREHOUSE = "warehouse", "انبار"

    class DealType(models.TextChoices):
        SALE = "sale", "فروش"
        RENT = "rent", "اجاره"
        MORTGAGE = "mortgage", "رهن"
        RENT_MORTGAGE = "rent_mortgage", "رهن و اجاره"

    class Status(models.TextChoices):
        AVAILABLE = "available", "موجود"
        RESERVED = "reserved", "رزرو شده"
        SOLD = "sold", "فروخته شده"
        RENTED = "rented", "اجاره داده شده"
        INACTIVE = "inactive", "غیرفعال"

    # اطلاعات اصلی
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)

    property_type = models.CharField(
        max_length=30,
        choices=PropertyType.choices
    )

    deal_type = models.CharField(
        max_length=30,
        choices=DealType.choices
    )

    description = models.TextField(blank=True)

    # اطلاعات ساختمان
    area = models.PositiveIntegerField(help_text="متراژ به متر مربع")
    bedrooms = models.PositiveSmallIntegerField(default=0)
    bathrooms = models.PositiveSmallIntegerField(default=0)

    floor = models.IntegerField(default=0)
    total_floors = models.PositiveSmallIntegerField(default=0)

    year_built = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    units_per_floor = models.PositiveSmallIntegerField(
        default=1
    )

    # قیمت
    price = models.DecimalField(
        max_digits=18,
        decimal_places=0,
        null=True,
        blank=True
    )

    deposit = models.DecimalField(
        max_digits=18,
        decimal_places=0,
        null=True,
        blank=True
    )

    monthly_rent = models.DecimalField(
        max_digits=18,
        decimal_places=0,
        null=True,
        blank=True
    )

    price_per_meter = models.DecimalField(
        max_digits=18,
        decimal_places=0,
        null=True,
        blank=True
    )

    # موقعیت
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    neighborhood = models.CharField(
        max_length=100,
        blank=True
    )

    address = models.TextField(blank=True)

    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True
    )

    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True
    )

    # امکانات
    parking = models.BooleanField(default=False)
    elevator = models.BooleanField(default=False)
    storage = models.BooleanField(default=False)
    balcony = models.BooleanField(default=False)
    furnished = models.BooleanField(default=False)
    air_conditioning = models.BooleanField(default=False)
    central_heating = models.BooleanField(default=False)

    # وضعیت
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE
    )

    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)

    # مشاور
    agent = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="properties"
    )

    # زمان‌ها
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["property_type"]),
            models.Index(fields=["deal_type"]),
            models.Index(fields=["city"]),
            models.Index(fields=["neighborhood"]),
            models.Index(fields=["price"]),
            models.Index(fields=["area"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)

        if self.area and self.price:
            self.price_per_meter = self.price / self.area

        super().save(*args, **kwargs)


class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="properties/%Y/%m/"
    )

    alt_text = models.CharField(
        max_length=200,
        blank=True
    )

    is_main = models.BooleanField(default=False)

    order = models.PositiveSmallIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return f"{self.property.title} - Image"


class PropertyFeature(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="features"
    )

    name = models.CharField(max_length=100)
    value = models.CharField(
        max_length=200,
        blank=True
    )

    class Meta:
        unique_together = ["property", "name"]

    def __str__(self):
        return f"{self.property.title} - {self.name}"


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites"
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="favorited_by"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "property"],
                name="unique_user_property_favorite"
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.property.title}"


class PropertyView(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="views"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    viewed_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"View - {self.property.title}"
