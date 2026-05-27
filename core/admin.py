from django.contrib import admin

from .models import Booking, Category, Comment, Favorite, Profile, Tour


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "phone")
    list_filter = ("role",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ("place", "country", "category", "price", "capacity", "days", "is_active", "is_featured")
    list_filter = ("category", "is_active", "is_featured")
    search_fields = ("title", "country", "place")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("user", "tour", "travel_date", "people", "status", "total_price")
    list_filter = ("status", "travel_date")
    search_fields = ("user__username", "tour__place", "tour__country")


admin.site.register(Comment)
admin.site.register(Favorite)
