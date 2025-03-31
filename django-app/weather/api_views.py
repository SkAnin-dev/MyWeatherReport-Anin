# API viewsets only for My Weather Report project.
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from .models import City, WeatherReport
from .serializers import CitySerializer, WeatherReportSerializer

# CityViewSet handles CRUD operations for City objects.
class CityViewSet(viewsets.ModelViewSet):
    serializer_class = CitySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # Return all cities ordered by name.
        return City.objects.all().order_by('name')

    # Custom action to retrieve a city by its name (case-insensitive).
    @action(detail=False, methods=['get'], url_path='by-name/(?P<name>[^/.]+)')
    def retrieve_by_name(self, request, name=None):
        city = get_object_or_404(City, name__iexact=name)
        serializer = self.get_serializer(city)
        return Response(serializer.data)

# WeatherReportViewSet handles CRUD operations for WeatherReport objects.
class WeatherReportViewSet(viewsets.ModelViewSet):
    queryset = WeatherReport.objects.all().order_by('-last_updated')
    serializer_class = WeatherReportSerializer
    permission_classes = [permissions.AllowAny]

    # Custom action to retrieve the latest weather report for a specific city.
    @action(detail=False, methods=['get'], url_path='latest/(?P<city_id>[^/.]+)')
    def latest_by_city(self, request, city_id=None):
        city = get_object_or_404(City, pk=city_id)
        weather_report = city.weather_reports.order_by('-last_updated').first()
        if not weather_report:
            raise ValidationError("No weather reports available for this city.")
        serializer = self.get_serializer(weather_report)
        return Response(serializer.data)
