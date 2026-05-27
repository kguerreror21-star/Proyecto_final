from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("tours/", views.TourListView.as_view(), name="tour_list"),
    path("tours/crear/", views.TourCreateView.as_view(), name="tour_create"),
    path("tours/<int:pk>/", views.TourDetailView.as_view(), name="tour_detail"),
    path("tours/<int:pk>/editar/", views.TourUpdateView.as_view(), name="tour_update"),
    path("tours/<int:pk>/eliminar/", views.TourDeleteView.as_view(), name="tour_delete"),
    path("tours/<int:pk>/reservar/", views.BookingCreateView.as_view(), name="booking_create"),
    path("mis-reservas/", views.MyBookingsView.as_view(), name="my_bookings"),
    path("registro/", views.RegisterView.as_view(), name="register"),
    path("destinos/", views.StaticPageView.as_view(template_name="core/destination.html"), name="destinations"),
    path("acerca-de/", views.StaticPageView.as_view(template_name="core/about.html"), name="about"),
    path("contacto/", views.StaticPageView.as_view(template_name="core/contact.html"), name="contact"),
]
