import json

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_GET, require_POST

from .forms import OrderForm, RegisterForm
from .models import Location, Catch, Badge
from .services.gps import is_within_radius

from django.http import HttpResponse
from django.contrib.auth.models import User

def create_admin(request):
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@test.com", "admin123")
        return HttpResponse("Admin created")
    return HttpResponse("Admin already exists")

@require_GET
def location_list(request):
    locations = Location.objects.all().order_by("id")
    login_form = AuthenticationForm()
    register_form = RegisterForm()

    return render(
        request,
        "game/location_list.html",
        {
            "locations": locations,
            "login_form": login_form,
            "register_form": register_form,
        },
    )


@require_GET
def location_detail(request, location_id):
    location = get_object_or_404(Location, id=location_id)
    return render(request, "game/location_detail.html", {"location": location})


def auth_page(request):
    if request.user.is_authenticated:
        return redirect("location_list")

    login_form = AuthenticationForm()
    register_form = RegisterForm()

    if request.method == "POST":
        if "login_submit" in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)

            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect("location_list")

        elif "register_submit" in request.POST:
            register_form = RegisterForm(request.POST)

            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                return redirect("location_list")

    return render(
        request,
        "registration/auth.html",
        {
            "login_form": login_form,
            "register_form": register_form,
        },
    )


@login_required
@require_POST
def catch_location(request, location_id):
    location = get_object_or_404(Location, id=location_id)

    if Catch.objects.filter(user=request.user, location=location).exists():
        return JsonResponse(
            {
                "success": False,
                "error": "Вече си хванал тази локация.",
            },
            status=400,
        )

    try:
        data = json.loads(request.body)
        user_lat = float(data.get("latitude"))
        user_lon = float(data.get("longitude"))
    except (TypeError, ValueError, json.JSONDecodeError):
        return JsonResponse(
            {
                "success": False,
                "error": "Невалидни GPS данни.",
            },
            status=400,
        )

    is_valid, distance = is_within_radius(
        location.latitude,
        location.longitude,
        user_lat,
        user_lon,
        location.allowed_radius_m,
    )

    if not is_valid:
        return JsonResponse(
            {
                "success": False,
                "error": f"Не сте достатъчно близо. Разстояние: {distance:.1f} м.",
            },
            status=400,
        )

    Catch.objects.create(
        user=request.user,
        location=location,
        user_latitude=user_lat,
        user_longitude=user_lon,
        distance_m=distance,
    )

    return JsonResponse(
        {
            "success": True,
            "redirect_url": f"/orders/create/?location_id={location.id}&distance={round(distance, 1)}",
        }
    )


@login_required
def create_order(request):
    location_id = request.GET.get("location_id") or request.POST.get("location_id")
    distance = request.GET.get("distance") or request.POST.get("distance")

    if not location_id:
        return render(request, "game/error.html", {"message": "Липсва location_id."})

    location = get_object_or_404(Location, id=location_id)

    try:
        distance_value = float(distance)
    except (TypeError, ValueError):
        distance_value = 0.0

    if request.method == "POST":
        form = OrderForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.location = location
            order.distance_m = distance_value
            order.save()

            return render(
                request,
                "game/order_success.html",
                {"order": order},
            )
    else:
        form = OrderForm()

    return render(
        request,
        "game/order_form.html",
        {
            "form": form,
            "location": location,
            "distance": distance_value,
        },
    )


@login_required
def profile_view(request):
    catches_count = request.user.catches.count()
    orders_count = request.user.orders.count()

    latest_catches = request.user.catches.select_related("location").order_by("-created_at")[:5]
    latest_orders = request.user.orders.select_related("location").order_by("-created_at")[:5]

    return render(
        request,
        "game/profile.html",
        {
            "catches_count": catches_count,
            "orders_count": orders_count,
            "latest_catches": latest_catches,
            "latest_orders": latest_orders,
        },
    )


@login_required
def my_orders_view(request):
    orders = request.user.orders.select_related("location").order_by("-created_at")

    return render(
        request,
        "game/my_orders.html",
        {
            "orders": orders,
        },
    )


@login_required
def caught_places_view(request):
    badges = Badge.objects.all().prefetch_related("locations")
    catches = request.user.catches.select_related("location", "location__badge")

    unlocked_badge_ids = []

    for catch in catches:
        if catch.location.badge:
            unlocked_badge_ids.append(catch.location.badge.id)

    return render(
        request,
        "game/caught_places.html",
        {
            "badges": badges,
            "unlocked_badge_ids": unlocked_badge_ids,
            "unlocked_count": len(set(unlocked_badge_ids)),
        },
    )