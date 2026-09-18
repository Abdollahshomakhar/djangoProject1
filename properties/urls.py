from django.urls import path

from . import views

app_name = "properties"

urlpatterns = [
    path("map/", views.properties_map, name="properties_map"),

    path(
        "",
        views.property_list,
        name="property_list",
    ),

    path(
        "search/",
        views.property_search,
        name="property_search",
    ),

    path(
        "my-properties/",
        views.my_properties,
        name="my_properties",
    ),

    path(
        "<int:pk>/update/",
        views.property_update,
        name="property_update",
    ),

    path(
        "<int:pk>/images/",
        views.property_images,
        name="property_images",
    ),

    path(
        "<int:pk>/contact/",
        views.property_contact,
        name="property_contact",
    ),
    path(
        "new/",
        views.property_create,
        name="property_create",
    ),
    path(
        "<slug:slug>/",
        views.property_detail,
        name="property_detail",
    ),

]
