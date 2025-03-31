import threading
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import City
from .views import DEFAULT_CITIES

# Global variable hold timer.
default_timer = None

def re_add_missing_defaults():
    global default_timer
    default_timer = None  # Clear timer
    # Iterate over each default city and create if missing.
    for city_name in DEFAULT_CITIES:
        if not City.objects.filter(name__iexact=city_name).exists():
            City.objects.create(name=city_name)

def schedule_default_restore():
    global default_timer
    # Cancel any existing timer
    if default_timer:
        default_timer.cancel()
    # Start new timer that calls re_add_missing_defaults after 10 seconds.
    default_timer = threading.Timer(10.0, re_add_missing_defaults)
    default_timer.start()

@receiver(post_delete, sender=City)
def restore_default_cities(sender, instance, **kwargs):
    # Check if any default city is missing.
    missing = any(not City.objects.filter(name__iexact=city_name).exists() for city_name in DEFAULT_CITIES)
    if missing:
        schedule_default_restore()