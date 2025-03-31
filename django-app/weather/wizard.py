# Data_wizard can be used during development.


import data_wizard
from .models import City, WeatherReport

# Register the City and WeatherReport models with data_wizard
data_wizard.register(City)
data_wizard.register(WeatherReport)
