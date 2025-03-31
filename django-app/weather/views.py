# Views for My Weather Report project.
from django.http import JsonResponse, HttpResponseForbidden
from django.views import View
from django.views.generic import ListView
from .models import City
from .forms import CityForm
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views.decorators.http import require_GET
import requests

@csrf_exempt  # Allow anonymous access for testing
@require_GET
@ensure_csrf_cookie
def set_csrf_cookie(request):
    return JsonResponse({'detail': 'CSRF cookie set.'})

@csrf_exempt  # Can remove this decorator in production if you want to enforce CSRF
@require_GET
def weather_proxy(request, city_name):
    # Note: In production, can consider adding error handling and caching.
    apikey = '83MPJTJKXE4NAFC8UB3TK53YA'
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city_name}?unitGroup=metric&key={apikey}&contentType=json"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        return JsonResponse({'error': 'Unable to retrieve data', 'details': str(e)}, status=500)
    
    return JsonResponse(data)

# List of default cities.
DEFAULT_CITIES = ['Tokyo', 'New York', 'London']

# CityListView: Displays list of cities as weather cards.
class CityListView(ListView):
    model = City
    template_name = 'cities/city_list.html'
    context_object_name = 'cities'

    def get_queryset(self):
        # With signal in place, defaults will be restored automatically
        return City.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for city in context['cities']:
            city.report_count = city.weather_reports.count()  # if applicable
        return context

# AJAX view for adding a new city.
class CityCreateAjaxView(View):
    @csrf_exempt  # Only for testing—remove if enforcing CSRF in production.
    def post(self, request, *args, **kwargs):
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.save(commit=False)
            # Optionally, associate city with the current user if needed.
            city.save()
            return JsonResponse({
                'status': 'success',
                'city': {'id': city.id, 'name': city.name}
            })
        else:
            return JsonResponse({
                'status': 'error',
                'errors': form.errors
            }, status=400)

# AJAX view for deleting a city.
class CityDeleteAjaxView(View):
    # For convenience, handle POST by routing it to delete.
    def post(self, request, pk, *args, **kwargs):
        return self.delete(request, pk, *args, **kwargs)
    
    def delete(self, request, pk, *args, **kwargs):
        try:
            city = City.objects.get(pk=pk)
        except City.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'City not found.'}, status=404)
        city.delete()
        return JsonResponse({'status': 'success'})
