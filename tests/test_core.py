import datetime as dt

import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from core.models import Booking, Category, Tour


@pytest.fixture
def category():
    return Category.objects.create(name="Aventura", slug="aventura")


@pytest.fixture
def tour(category):
    return Tour.objects.create(
        category=category,
        title="Yellowstone salvaje",
        country="Estados Unidos",
        place="Parque Nacional Yellowstone",
        description="Tour de prueba",
        price=500,
        capacity=12,
        days=5,
        image="tours/tour-6.avif",
        is_active=True,
    )


@pytest.mark.django_db
def test_profile_is_created_for_new_user():
    user = User.objects.create_user(username="cliente@example.com", password="Password123")

    assert user.profile.role == "tourist"
    assert user.profile.can_manage_tours is False


@pytest.mark.django_db
def test_tour_list_shows_active_tours(client, tour):
    response = client.get(reverse("tour_list"))

    assert response.status_code == 200
    assert "Parque Nacional Yellowstone" in response.content.decode()
    assert tour.get_absolute_url() in response.content.decode()


@pytest.mark.django_db
def test_tour_detail_opens_from_absolute_url(client, tour):
    response = client.get(tour.get_absolute_url())

    assert response.status_code == 200
    assert "Parque Nacional Yellowstone" in response.content.decode()
    assert tour.image.url in response.content.decode()


@pytest.mark.django_db
def test_login_redirects_to_home_with_real_authentication(client):
    User.objects.create_user(username="cliente@example.com", password="StrongPass123!")

    response = client.post(
        reverse("login"),
        {"username": "cliente@example.com", "password": "StrongPass123!"},
    )

    assert response.status_code == 302
    assert response.url == reverse("home")


@pytest.mark.django_db
def test_login_respects_next_redirect(client, tour):
    User.objects.create_user(username="cliente@example.com", password="StrongPass123!")

    response = client.post(
        f"{reverse('login')}?next={tour.get_absolute_url()}",
        {"username": "cliente@example.com", "password": "StrongPass123!"},
    )

    assert response.status_code == 302
    assert response.url == tour.get_absolute_url()


@pytest.mark.django_db
def test_register_creates_user_and_logs_in(client):
    response = client.post(
        reverse("register"),
        {
            "first_name": "Ana",
            "email": "ana@example.com",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        },
    )

    assert response.status_code == 302
    assert User.objects.filter(username="ana@example.com").exists()


@pytest.mark.django_db
def test_authenticated_user_can_book_tour(client, tour):
    user = User.objects.create_user(username="cliente@example.com", password="StrongPass123!")
    client.force_login(user)

    response = client.post(
        reverse("booking_create", args=[tour.pk]),
        {
            "travel_date": (dt.date.today() + dt.timedelta(days=10)).isoformat(),
            "people": 2,
            "notes": "Viaje familiar",
        },
    )

    assert response.status_code == 302
    booking = Booking.objects.get(user=user, tour=tour)
    assert booking.people == 2
    assert booking.total_price == 1000


@pytest.mark.django_db
def test_capacity_validation_blocks_oversized_booking(client, tour):
    user = User.objects.create_user(username="cliente@example.com", password="StrongPass123!")
    client.force_login(user)

    response = client.post(
        reverse("booking_create", args=[tour.pk]),
        {
            "travel_date": (dt.date.today() + dt.timedelta(days=10)).isoformat(),
            "people": 99,
            "notes": "",
        },
    )

    assert response.status_code == 200
    assert Booking.objects.count() == 0
    assert "capacidad disponible" in response.content.decode()


@pytest.mark.django_db
def test_original_footer_content_is_rendered_on_main_pages(client, tour):
    urls = [
        reverse("home"),
        reverse("tour_list"),
        reverse("login"),
        reverse("register"),
        reverse("tour_detail", args=[tour.pk]),
        reverse("about"),
        reverse("contact"),
    ]

    for url in urls:
        response = client.get(url)
        content = response.content.decode()

        assert response.status_code == 200
        assert "Agencia de viajes especializada" in content
        assert "info@adventurero.com" in content
        assert "Cra. 10 # 20-30, Bogota, Colombia" in content
        assert "payment-methods.png" in content
