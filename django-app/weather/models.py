# Models for My Weather Report project.
from django.db import models

# City Model.
# Represents a city for which weather data is available.
class City(models.Model):
    # Name of the city. Marked as unique to prevent duplicate entries.
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Name of the city for which weather data is available."
    )
    # Automatically records the date and time when the city was added.
    added_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the city was added to the database."
    )

    def __str__(self):
        # Returns the city's name as its string representation.
        return self.name


# WeatherReport Model.
# Stores weather details for a given city.
class WeatherReport(models.Model):
    # Links the weather report to a specific city.
    # If city is deleted, all associated weather reports will be removed (CASCADE).
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='weather_reports',
        help_text="Foreign key linking this weather report to a city."
    )
    # Temperature recorded in Celsius.
    temperature = models.FloatField(
        help_text="Recorded temperature in Celsius."
    )
    # A short description of the weather condition (e.g., Clear, Rainy, Cloudy).
    condition = models.CharField(
        max_length=100,
        help_text="Short description of the current weather condition."
    )
    # Field to store the URL of an icon representing the weather condition.
    icon_url = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        help_text="URL for a weather icon image."
    )
    # Automatically updated timestamp for when the weather report was last modified.
    last_updated = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp for the last update of this weather report."
    )

    def __str__(self):
        # Returns string representation that includes the city name, temperature, and condition.
        return f"{self.city.name} - {self.temperature}°C, {self.condition}"
