from django.db import models
from django.contrib.auth.models import User


class Badge(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="badges/", blank= True, null= True)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=120)
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField(blank=True)
    allowed_radius_m = models.PositiveIntegerField(default=120)

    badge = models.ForeignKey(
        Badge,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="locations"
    )

    def __str__(self):
        return self.name


class Catch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="catches")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="catches")
    user_latitude = models.FloatField()
    user_longitude = models.FloatField()
    distance_m = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "location"], name="unique_user_location_catch")
        ]

    def __str__(self):
        return f"{self.user.username} - {self.location.name} - {self.distance_m:.1f} m"


class Order(models.Model):
    DELIVERY_CHOICES = [
        ("econt", "Econt Office"),
        ("address", "Personal Address"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="orders")
    customer_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_CHOICES)
    delivery_details = models.TextField()
    distance_m = models.FloatField()
    status = models.CharField(max_length=20, default="new")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} - {self.location.name}"