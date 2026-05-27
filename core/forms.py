from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Booking, Comment, Tour


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Correo electronico")
    first_name = forms.CharField(label="Nombre", max_length=150, required=False)

    class Meta:
        model = User
        fields = ("first_name", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe una cuenta con este correo.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = (
            "category",
            "title",
            "country",
            "place",
            "description",
            "price",
            "capacity",
            "days",
            "image",
            "is_featured",
            "is_active",
        )


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ("travel_date", "people", "notes")
        widgets = {"travel_date": forms.DateInput(attrs={"type": "date"})}

    def __init__(self, *args, tour=None, **kwargs):
        self.tour = tour
        super().__init__(*args, **kwargs)

    def clean_people(self):
        people = self.cleaned_data["people"]
        if self.tour and people > self.tour.capacity:
            raise forms.ValidationError("La cantidad supera la capacidad disponible del tour.")
        return people


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("rating", "body")
        widgets = {"rating": forms.NumberInput(attrs={"min": 1, "max": 5})}
