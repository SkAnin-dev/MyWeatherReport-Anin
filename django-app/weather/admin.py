from django.contrib import admin
from .models import City, WeatherReport

# Admin panel integration for the City model.
# Allows administrators to view and manage cities easily.
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'added_at')  # Displays city name and when added.
    search_fields = ('name',)            # Enables search functionality on city name.
    list_filter = ('added_at',)          # Adds filter for added_at field.

# Admin panel integration for the WeatherReport model.
# Helps admins manage weather reports and view relevant details.
@admin.register(WeatherReport)
class WeatherReportAdmin(admin.ModelAdmin):
    list_display = ('city', 'temperature', 'condition', 'last_updated')  # Key weather info to display.
    list_filter = ('condition', 'last_updated')                          # Filter options for condition and update time.
    search_fields = ('city__name', 'condition')                          # Searchable by city name and weather condition.
