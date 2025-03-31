# Serializers for My Weather Report project.

from rest_framework import serializers
from .models import City, WeatherReport

# City model's serializer.
# Handles both serialization and deserialization for City objects.
# Includes nested list of weather reports for the city.
class CitySerializer(serializers.ModelSerializer):
    # Nested field to show all weather reports associated with the city.
    weather_reports = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = City
        # Fields: id, name, added_at, and nested weather reports.
        fields = ['id', 'name', 'added_at', 'weather_reports']
        # 'added_at' and 'weather_reports' are read-only.
        read_only_fields = ['added_at', 'weather_reports']

    # Returns all weather reports for this city using WeatherReportSerializer.
    def get_weather_reports(self, obj):
        reports = obj.weather_reports.all().order_by('-last_updated')
        return WeatherReportSerializer(reports, many=True).data


# WeatherReport model's serializer.
# Manages serialization of weather report objects.
class WeatherReportSerializer(serializers.ModelSerializer):
    # Read-only field to show city's name from the related City model.
    city_name = serializers.ReadOnlyField(source='city.name')

    class Meta:
        model = WeatherReport
        # Fields: id, city (foreign key), city_name, temperature, condition, icon_url, and last_updated.
        fields = ['id', 'city', 'city_name', 'temperature', 'condition', 'icon_url', 'last_updated']
        # 'last_updated' and 'city_name' are automatically managed/read-only.
        read_only_fields = ['last_updated', 'city_name']
