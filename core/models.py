from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


class Profile(models.Model):
    class Role(models.TextChoices):
        ADMIN = "admin", "Administrador"
        TOURIST = "tourist", "Cliente/Turista"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.TOURIST)
    phone = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    @property
    def can_manage_tours(self):
        return self.role == self.Role.ADMIN or self.user.is_staff


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Tour(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="tours")
    title = models.CharField(max_length=160)
    country = models.CharField(max_length=90)
    place = models.CharField(max_length=160)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    capacity = models.PositiveIntegerField(default=1)
    days = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to="tours/", blank=True, help_text="Imagen del tour")
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["country", "place"]

    def __str__(self):
        return f"{self.place}, {self.country}"

    def get_absolute_url(self):
        return reverse("tour_detail", kwargs={"pk": self.pk})


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pendiente"
        CONFIRMED = "confirmed", "Confirmada"
        CANCELLED = "cancelled", "Cancelada"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="bookings")
    travel_date = models.DateField()
    people = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Reserva de {self.user} para {self.tour}"

    @property
    def total_price(self):
        return self.people * self.tour.price


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="comments")
    rating = models.PositiveSmallIntegerField(default=5)
    body = models.TextField()
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} califico {self.tour} con {self.rating}"


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="favorites")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "tour")

    def __str__(self):
        return f"{self.user} guarda {self.tour}"
