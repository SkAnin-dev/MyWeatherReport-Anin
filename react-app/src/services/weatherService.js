export const fetchWeatherDataForCity = (cityName) => {
  const apikey = '83MPJTJKXE4NAFC8UB3TK53YA';
  const apiUrl = `https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/${encodeURIComponent(cityName)}?unitGroup=metric&key=${apikey}&contentType=json`;
  return fetch(apiUrl).then(res => res.json());
};
