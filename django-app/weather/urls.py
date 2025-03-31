from django.contrib import admin, messages
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

# Import API viewsets for the weather project.
from weather.api_views import CityViewSet, WeatherReportViewSet
# Import templated and AJAX views for the weather webpage.
from weather.views import (
    CityListView,
    CityCreateAjaxView,
    CityDeleteAjaxView,
    set_csrf_cookie,  # CSRF cookie view
    weather_proxy,
)

def test_message_view(request):
    messages.success(request, "Test message works!")
    return redirect('city-list')

# Main router for API endpoints.
router = DefaultRouter()
router.register(r'cities', CityViewSet, basename='city')
router.register(r'weather-reports', WeatherReportViewSet, basename='weatherreport')

# Custom API Root View to list all available endpoints.
class APIRootView(APIView):
    def get(self, request):
        base_url = request.build_absolute_uri('/api/')
        return Response({
            "cities": f"{base_url}cities/",
            "weather_reports": f"{base_url}weather-reports/",
        })

urlpatterns = [
    # Utility route for testing messages.
    path('test-message/', test_message_view, name='test-message'),
    
    # Admin route.
    path('admin/', admin.site.urls),
    # Data wizard routes (optional for development/testing).
    path('datawizard/', include('data_wizard.urls')),
    
    # API routes.
    path('api/', include(router.urls)),  # Auto-generated API endpoints.
    path('api/', APIRootView.as_view(), name='api-root'),
    
    # Templated view for displaying cities.
    path('', CityListView.as_view(), name='city-list'),
    path('cities/', CityListView.as_view(), name='city-list'),
    
    # AJAX endpoints for dynamic city creation and deletion.
    path('ajax/cities/add/', CityCreateAjaxView.as_view(), name='add-city'),
    path('ajax/cities/<int:pk>/delete/', CityDeleteAjaxView.as_view(), name='ajax-city-delete'),
    
    #path('api/reset-defaults/', reset_defaults, name='reset-defaults'), # Default city path

    # New CSRF cookie endpoint.
    path('set-csrf/', set_csrf_cookie, name='set-csrf'),
    path('proxy/weather/<str:city_name>/', weather_proxy, name='weather-proxy'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
