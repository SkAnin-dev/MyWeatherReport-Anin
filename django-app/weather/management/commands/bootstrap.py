# Bootsrap for sample data.
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from weather.models import City, WeatherReport

class Command(BaseCommand):
    help = 'Bootstrap MyWeatherReport for first-time deployment'

    def handle(self, *args, **options):
        try:
            self.stdout.write("Starting bootstrap process for MyWeatherReport...")

            # Step 1: Create sample cities.
            sample_cities = [
                {"name": "London"},
                {"name": "New York"},
                {"name": "Tokyo"},
                {"name": "Sydney"},
                {"name": "Paris"},
                {"name": "Dhaka"},
                {"name": "Thailand"},
                {"name": "Singapore"},
            ]
            created_cities = []
            self.stdout.write("Creating sample cities...")
            for city_data in sample_cities:
                city, created = City.objects.get_or_create(**city_data)
                if created:
                    self.stdout.write(f"Created city: {city.name}")
                else:
                    self.stdout.write(f"City already exists: {city.name}")
                created_cities.append(city)

            # Step 2: Create sample weather reports for each city.
            self.stdout.write("Creating sample weather reports...")
            sample_reports = [
                {
                    "city": created_cities[0],
                    "temperature": 15.0,
                    "condition": "Cloudy",
                    "icon_url": "http://example.com/cloudy.png"
                },
                {
                    "city": created_cities[1],
                    "temperature": 22.0,
                    "condition": "Clear",
                    "icon_url": "http://example.com/clear.png"
                },
                {
                    "city": created_cities[2],
                    "temperature": 28.0,
                    "condition": "Sunny",
                    "icon_url": "http://example.com/sunny.png"
                },
                {
                    "city": created_cities[3],
                    "temperature": 18.0,
                    "condition": "Rainy",
                    "icon_url": "http://example.com/rainy.png"
                },
                {
                    "city": created_cities[4],
                    "temperature": 20.0,
                    "condition": "Partly Cloudy",
                    "icon_url": "http://example.com/partly_cloudy.png"
                },
                {
                    "city": created_cities[5],
                    "temperature": 20.0,
                    "condition": "Partly Cloudy",
                    "icon_url": "http://example.com/partly_cloudy.png"
                },
                {
                    "city": created_cities[6],
                    "temperature": 20.0,
                    "condition": "Partly Cloudy",
                    "icon_url": "http://example.com/partly_cloudy.png"
                },
                {
                    "city": created_cities[7],
                    "temperature": 20.0,
                    "condition": "Partly Cloudy",
                    "icon_url": "http://example.com/partly_cloudy.png"
                },
            ]
            for report_data in sample_reports:
                report, created = WeatherReport.objects.get_or_create(
                    city=report_data["city"],
                    temperature=report_data["temperature"],
                    condition=report_data["condition"],
                    icon_url=report_data["icon_url"]
                )
                if created:
                    self.stdout.write(f"Created weather report for {report.city.name}")
                else:
                    self.stdout.write(f"Weather report for {report.city.name} already exists.")

            self.stdout.write(self.style.SUCCESS("Bootstrap completed successfully!"))

        except IntegrityError as e:
            self.stderr.write(self.style.ERROR(f"Integrity error during bootstrap: {str(e)}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Unexpected error: {str(e)}"))
