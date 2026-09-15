from django.shortcuts import render
from .forms import AvailabilityForm
from .models import Room, Reservation
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from .models import Room, Reservation
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def home(request):
    form = AvailabilityForm(request.GET or None)
    available_rooms = None

    if form.is_valid():
        check_in = form.cleaned_data["check_in"]
        check_out = form.cleaned_data["check_out"]
        guest_count = form.cleaned_data["guest_count"]

        rooms = Room.objects.filter(
            is_active=True,
            capacity__gte=guest_count
        )

        conflicting_reservations = Reservation.objects.filter(
                check_in__lt=check_out,
                check_out__gt=check_in
            ).exclude(
                status="cancelled")

        reserved_room_ids = conflicting_reservations.values_list(
            "room_id",
            flat=True
        )

        available_rooms = rooms.exclude(
            id__in=reserved_room_ids
        )

    return render(
        request,
        "booking/home.html",
        {
            "form": form,
            "available_rooms": available_rooms,
        }
    )

@login_required
def book_room(request, room_id):

    room = get_object_or_404(
        Room,
        id=room_id
    )

    if request.method == "POST":

        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")
        guest_count = request.POST.get("guest_count")

    else:

        check_in = request.GET.get("check_in")
        check_out = request.GET.get("check_out")
        guest_count = request.GET.get("guest_count")


    check_in_date = datetime.strptime(
        check_in,
        "%Y-%m-%d"
    ).date()

    check_out_date = datetime.strptime(
        check_out,
        "%Y-%m-%d"
    ).date()


    nights = (
        check_out_date - check_in_date
    ).days

    total_price = (
        nights * room.price_per_night
    )


    if request.method == "POST":

        Reservation.objects.create(
            user=request.user,
            room=room,
            guest_count=guest_count,
            check_in=check_in_date,
            check_out=check_out_date,
            total_price=total_price
        )

        return redirect("booking:home")


    return render(
        request,
        "booking/book_room.html",
        {
            "room": room,
            "check_in": check_in,
            "check_out": check_out,
            "guest_count": guest_count,
            "nights": nights,
            "total_price": total_price,
        }
    )
def success(request):
    return render(request,"booking/success.html")
@login_required
def reservations(request):

    reservations = Reservation.objects.filter(
        user=request.user
    ).exclude(
        status="cancelled"
    ).order_by("-created_at")

    return render(
        request,
        "booking/reservations.html",
        {
            "reservations": reservations
        }
    )
@login_required
def cancel_reservation(request, reservation_id):

    reservation = get_object_or_404(
        Reservation,
        id=reservation_id,
        user=request.user
    )

    if request.method == "POST":
        reservation.status = "cancelled"
        reservation.save()

    return redirect("booking:reservations")

def signup(request):

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect("booking:home")

    else:
        form = UserCreationForm()

    return render(
        request,
        "registration/signup.html",
        {
            "form": form
        }
    )