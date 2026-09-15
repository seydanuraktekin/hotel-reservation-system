from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Room(models.Model):
    room_number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()
    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Room {self.room_number} - {self.room_type}"

class Reservation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE
    )

    guest_count = models.PositiveIntegerField()

    check_in = models.DateField()

    check_out = models.DateField()

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Room {self.room.room_number}"

    STATUS_CHOICES = [
        ("upcoming", "Upcoming"),
        ("cancelled", "Cancelled"),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="upcoming"
    )

@property
def current_status(self):
    if self.status == "cancelled":
        return "Cancelled"

    today = timezone.now().date()

    if today < self.check_in:
        return "Upcoming"

    elif self.check_in <= today < self.check_out:
        return "Active"

    else:
        return "Completed"