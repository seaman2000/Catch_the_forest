from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.location_list, name="location_list"),
    path("locations/<int:location_id>/", views.location_detail, name="location_detail"),
    path("locations/<int:location_id>/catch/", views.catch_location, name="catch_location"),
    path("orders/create/", views.create_order, name="create_order"),

    path("auth/", views.auth_page, name="auth"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    path("profile/", views.profile_view, name="profile"),
    path("my-orders/", views.my_orders_view, name="my_orders"),
    path("caught-places/", views.caught_places_view, name="caught_places"),
]