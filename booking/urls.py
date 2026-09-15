from django.urls import path
from . import views

app_name = "booking"

urlpatterns = [ path("",views.home, name="home"),
                path("book/<int:room_id>/",views.book_room,
                    name="book_room"),
                path("success/",views.success, name="success"),
                path("reservations/",views.reservations,name="reservations"),
                path("cancel/<int:reservation_id>/",views.cancel_reservation,name="cancel_reservation"),
                path( "signup/",views.signup,name="signup"),

]