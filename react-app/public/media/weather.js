// Set default cursor style
document.body.style.cursor = "default";

// Visual Crossing API settings for marquee update
const apikey = 'BP8GPRYV53UQ56SHJR5EFCJ77';
const myCity = 'Guildford';
const marqueeApiUrl = `https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/${encodeURIComponent(myCity)}?unitGroup=metric&key=${apikey}&contentType=json`;

// Update marquee with live weather data, or show error if data isn't pulled.
fetch(marqueeApiUrl)
  .then((response) => {
    if (!response.ok) {
      throw new Error("Error fetching marquee data");
    }
    return response.json();
  })
  .then((data) => {
    const cityInfo = document.getElementById('cityinfo');
    if (data && data.currentConditions) {
      let todayCondition = ` Now: ${data.currentConditions.temp}℃ ${data.currentConditions.conditions}`;
      let tmrCondition = "";
      if (data.days && data.days.length > 1) {
        tmrCondition = ` Tomorrow: ${data.days[1].temp}℃ ${data.days[1].conditions}`;
      }
      cityInfo.innerHTML = myCity.concat(todayCondition, '; ', tmrCondition);
    } else {
      // If data is empty or not as expected, show error message.
      cityInfo.innerHTML = "Error loading marquee data.";
    }
  })
  .catch(function(error) { 
    const cityInfo = document.getElementById('cityinfo');
    cityInfo.innerHTML = "Error loading marquee data.";
  });

// onPageRefresh: show progress cursor
function onPageRefresh() { 
  document.body.style.cursor = "progress"; 
  const cursorStyle = document.createElement('style'); 
  cursorStyle.innerHTML = '*{cursor: progress;}'; 
  cursorStyle.id = 'cursor-style'; 
  document.head.appendChild(cursorStyle); 
  return true; 
}

function removeCursorStyle() {
  const styleEl = document.getElementById("cursor-style");
  if (styleEl) styleEl.remove();
}

// Update individual weather card based on city name using timeline endpoint
function updateCityCard(card, cityName) {
  const apiUrl = `https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/${encodeURIComponent(cityName)}?unitGroup=metric&key=${apikey}&contentType=json`;
  fetch(apiUrl)
    .then((response) => response.json())
    .then((data) => {
      const current = data.currentConditions || data.days?.[0];
      if (current) {
        card.querySelector('.subtitle').textContent = current.temp + "° C";
        card.querySelector('.condition').textContent = current.conditions;
      } else {
        card.querySelector('.subtitle').textContent = "N/A";
        card.querySelector('.condition').textContent = "No Data";
      }
    })
    .catch((error) => {
      console.error("Error updating card for " + cityName, error);
    });
}

// Update all weather cards on page load
document.querySelectorAll('.city-box').forEach((card) => {
  const cityNameElement = card.querySelector('.title');
  const cityName = cityNameElement ? cityNameElement.textContent.trim() : null;
  if (cityName) {
    updateCityCard(card, cityName);
  }
});

// Helper function to get CSRF token for AJAX requests.
function getCSRFToken() {
  return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// Helper: Create Bulma notification element
function createNotification(message, bulmaClass) {
  const notification = document.createElement("div");
  notification.className = `notification ${bulmaClass}`;
  notification.innerHTML = `<button class="delete"></button> ${message}`;
  notification.querySelector(".delete").addEventListener("click", () => {
    notification.remove();
  });
  return notification;
}
