from django.core.management.base import BaseCommand
from django.utils.text import slugify

from core.models import Category, Tour


TOURS = [
    ("Cultura", "Japon historico", "Japon", "Templo Kiyomizu-dera", 565, 10, 5, "tours/tour-1.avif", True),
    ("Cultura", "Castillos del Loira", "Francia", "Castillo de Chambord", 520, 12, 4, "tours/tour-2.avif", True),
    ("Cultura", "Historia de Londres", "Reino Unido", "Torre de Londres", 450, 8, 5, "tours/tour-3.avif", False),
    ("Cultura", "Roma clasica", "Italia", "Coliseo Romano y Foro", 300, 12, 2, "tours/tour-4.avif", False),
    ("Aventura", "Egipto monumental", "Egipto", "Piramides de Giza y Esfinge", 800, 20, 3, "tours/tour-5.avif", True),
    ("Aventura", "Yellowstone salvaje", "Estados Unidos", "Parque Nacional Yellowstone", 500, 12, 5, "tours/tour-6.avif", False),
]


class Command(BaseCommand):
    help = "Carga categorias y tours de demostracion para Adventurero."

    def handle(self, *args, **options):
        for category_name, title, country, place, price, capacity, days, image, featured in TOURS:
            category, _ = Category.objects.get_or_create(
                slug=slugify(category_name),
                defaults={"name": category_name, "description": f"Tours de {category_name.lower()}"},
            )
            Tour.objects.update_or_create(
                country=country,
                place=place,
                defaults={
                    "category": category,
                    "title": title,
                    "description": f"Explora {place} en {country} con guias expertos, itinerario organizado y soporte de Adventurero.",
                    "price": price,
                    "capacity": capacity,
                    "days": days,
                    "image": image,
                    "is_featured": featured,
                    "is_active": True,
                },
            )
        self.stdout.write(self.style.SUCCESS("Datos demo cargados correctamente."))
