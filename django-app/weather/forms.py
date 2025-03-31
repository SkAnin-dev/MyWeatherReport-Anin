#Forms for the My Weather Report project.

from django import forms
from .models import City, WeatherReport


# CityForm for creating a city.
class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name']
    
    # Custom clean method for the city name.
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            name = name.strip()
            # Additional validation can be added here if needed.
        return name


# WeatherReportForm for creating a weather report.
class WeatherReportForm(forms.ModelForm):
    class Meta:
        model = WeatherReport
        fields = ['city', 'temperature', 'condition', 'icon_url']
    
    # Validate temperature within a realistic range.
    def clean_temperature(self):
        temperature = self.cleaned_data.get('temperature')
        if temperature is not None:
            # Example: Enforce temperature range between -100°C and 100°C.
            if temperature < -100 or temperature > 100:
                raise forms.ValidationError("Temperature must be between -100 and 100°C.")
        return temperature

    # Validate that weather condition is provided.
    def clean_condition(self):
        condition = self.cleaned_data.get('condition')
        if not condition:
            raise forms.ValidationError("Weather condition cannot be empty.")
        return condition
