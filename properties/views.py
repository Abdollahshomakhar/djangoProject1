from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Property, PropertyImage, PropertyView


def property_list(request):
    properties = Property.objects.filter(
        is_published=True
    ).select_related("agent").prefetch_related("images")

    return render(
        request,
        "properties/property_list.html",
        {
            "properties": properties,
        }
    )


def property_detail(request, slug):
    property_obj = get_object_or_404(
        Property.objects.select_related("agent").prefetch_related(
            "images",
            "features",
        ),
        slug=slug,
        is_published=True,
    )

    property_view(request, property_obj)

    return render(
        request,
        "properties/property_detail.html",
        {
            "property": property_obj,
        }
    )


def property_search(request):
    properties = Property.objects.filter(
        is_published=True
    ).select_related("agent")

    query = request.GET.get("q", "").strip()
    city = request.GET.get("city", "").strip()
    neighborhood = request.GET.get("neighborhood", "").strip()
    property_type = request.GET.get("property_type", "").strip()
    deal_type = request.GET.get("deal_type", "").strip()

    min_price = request.GET.get("min_price", "").strip()
    max_price = request.GET.get("max_price", "").strip()

    min_area = request.GET.get("min_area", "").strip()
    max_area = request.GET.get("max_area", "").strip()

    bedrooms = request.GET.get("bedrooms", "").strip()

    if query:
        properties = properties.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(address__icontains=query)
            | Q(neighborhood__icontains=query)
            | Q(city__icontains=query)
        )

    if city:
        properties = properties.filter(city__icontains=city)

    if neighborhood:
        properties = properties.filter(
            neighborhood__icontains=neighborhood
        )

    if property_type:
        properties = properties.filter(
            property_type=property_type
        )

    if deal_type:
        properties = properties.filter(
            deal_type=deal_type
        )

    if min_price:
        try:
            properties = properties.filter(
                price__gte=min_price
            )
        except (ValueError, TypeError):
            pass

    if max_price:
        try:
            properties = properties.filter(
                price__lte=max_price
            )
        except (ValueError, TypeError):
            pass

    if min_area:
        try:
            properties = properties.filter(
                area__gte=min_area
            )
        except (ValueError, TypeError):
            pass

    if max_area:
        try:
            properties = properties.filter(
                area__lte=max_area
            )
        except (ValueError, TypeError):
            pass

    if bedrooms:
        try:
            properties = properties.filter(
                bedrooms__gte=bedrooms
            )
        except (ValueError, TypeError):
            pass

    return render(
        request,
        "properties/property_search.html",
        {
            "properties": properties,
            "query": query,
            "city": city,
            "neighborhood": neighborhood,
            "property_type": property_type,
            "deal_type": deal_type,
            "min_price": min_price,
            "max_price": max_price,
            "min_area": min_area,
            "max_area": max_area,
            "bedrooms": bedrooms,
        }
    )


@login_required
def property_update(request, pk):
    property_obj = get_object_or_404(
        Property,
        pk=pk,
        agent=request.user,
    )

    if request.method == "POST":
        property_obj.title = request.POST.get(
            "title",
            property_obj.title
        )

        property_obj.description = request.POST.get(
            "description",
            property_obj.description
        )

        property_obj.area = request.POST.get(
            "area",
            property_obj.area
        )

        property_obj.bedrooms = request.POST.get(
            "bedrooms",
            property_obj.bedrooms
        )

        property_obj.bathrooms = request.POST.get(
            "bathrooms",
            property_obj.bathrooms
        )

        property_obj.price = request.POST.get(
            "price",
            property_obj.price
        )

        property_obj.deposit = request.POST.get(
            "deposit",
            property_obj.deposit
        )

        property_obj.monthly_rent = request.POST.get(
            "monthly_rent",
            property_obj.monthly_rent
        )

        property_obj.city = request.POST.get(
            "city",
            property_obj.city
        )

        property_obj.neighborhood = request.POST.get(
            "neighborhood",
            property_obj.neighborhood
        )

        property_obj.address = request.POST.get(
            "address",
            property_obj.address
        )

        property_obj.save()

        return redirect(
            "properties:property_detail",
            slug=property_obj.slug,
        )

    return render(
        request,
        "properties/property_update.html",
        {
            "property": property_obj,
        }
    )


@login_required
def property_images(request, pk):
    property_obj = get_object_or_404(
        Property,
        pk=pk,
        agent=request.user,
    )

    if request.method == "POST":

        images = request.FILES.getlist("images")

        for image in images:
            PropertyImage.objects.create(
                property=property_obj,
                image=image,
            )

        return redirect(
            "properties:property_images",
            pk=property_obj.pk,
        )

    images = property_obj.images.all()

    return render(
        request,
        "properties/property_images.html",
        {
            "property": property_obj,
            "images": images,
        }
    )


@login_required
def my_properties(request):
    properties = Property.objects.filter(
        agent=request.user
    ).prefetch_related("images")

    return render(
        request,
        "properties/my_properties.html",
        {
            "properties": properties,
        }
    )


@login_required
def property_contact(request, pk):
    property_obj = get_object_or_404(
        Property,
        pk=pk,
        is_published=True,
    )

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        message = request.POST.get("message", "").strip()

        # فعلاً فقط پاسخ JSON می‌دهیم.
        # بعداً می‌توانیم اینجا سیستم پیام/تماس را اضافه کنیم.

        return JsonResponse(
            {
                "success": True,
                "message": "پیام شما با موفقیت ارسال شد.",
                "property": property_obj.title,
                "name": name,
                "phone": phone,
                "message_text": message,
            }
        )

    return render(
        request,
        "properties/property_contact.html",
        {
            "property": property_obj,
        }
    )


@login_required
def property_create(request):
    if request.method == "POST":

        def to_number(value):
            value = (value or "").strip()
            if not value:
                return None
            try:
                return float(value)
            except ValueError:
                return None

        property_obj = Property(
            agent=request.user,
            title=request.POST.get("title", ""),
            description=request.POST.get("description", ""),
            area=to_number(request.POST.get("area")),
            bedrooms=request.POST.get("bedrooms") or None,
            bathrooms=request.POST.get("bathrooms") or None,
            price=to_number(request.POST.get("price")),
            deposit=to_number(request.POST.get("deposit")),
            monthly_rent=to_number(request.POST.get("monthly_rent")),
            city=request.POST.get("city", ""),
            neighborhood=request.POST.get("neighborhood", ""),
            address=request.POST.get("address", ""),
        )

        property_obj.save()

        return redirect(
            "properties:property_images",
            pk=property_obj.pk,
        )

    return render(
        request,
        "properties/property_create.html",
        {}
    )


def property_view(request, property_obj):
    """
    ثبت بازدید از ملک
    """

    ip_address = request.META.get("REMOTE_ADDR")

    PropertyView.objects.create(
        property=property_obj,
        user=request.user if request.user.is_authenticated else None,
        ip_address=ip_address,
    )


from django.urls import reverse
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Property, PropertyImage, PropertyView


def properties_map(request):
    properties = Property.objects.filter(
        is_published=True,
        latitude__isnull=False,
        longitude__isnull=False,
    )

    properties_json = [
        {
            "lat": float(p.latitude),
            "lng": float(p.longitude),
            "title": p.title,
            "url": reverse("properties:property_detail", args=[p.slug]),
        }
        for p in properties
    ]

    return render(
        request,
        "properties/properties_map.html",
        {
            "properties": properties,
            "properties_json": properties_json,
        }
    )
