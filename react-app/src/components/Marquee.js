import React, { useEffect } from 'react';
import { PROXY } from '../constant';

/* eslint-disable jsx-a11y/no-distracting-elements */
const Marquee = () => {
  useEffect(() => {
    const myCity = 'Guildford';
    const proxyUrl = `${PROXY}weather/${encodeURIComponent(myCity)}/`;

    fetch(proxyUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error("Error fetching marquee data");
        }
        return response.json();
      })
      .then(data => {
        const cityInfo = document.getElementById('cityinfo');
        if (data && data.currentConditions) {
          let todayCondition = ` Now: ${data.currentConditions.temp}℃ ${data.currentConditions.conditions}`;
          let tmrCondition = "";
          if (data.days && data.days.length > 1) {
            tmrCondition = ` Tomorrow: ${data.days[1].temp}℃ ${data.days[1].conditions}`;
          }
          cityInfo.innerHTML = myCity.concat(todayCondition, '; ', tmrCondition);
        } else {
          cityInfo.innerHTML = "Error loading marquee data.";
        }
      })
      .catch(error => {
        const cityInfo = document.getElementById('cityinfo');
        cityInfo.innerHTML = "Error loading marquee data.";
      });
  }, []);

  return (
    <section className="hero is-info">
      <marquee behavior="scroll" direction="left" id="cityinfo">
        Guildford Now: 11.1℃ Clear; Tomorrow: 5.3℃ Rain, Partially cloudy
      </marquee>
    </section>
  );
};

export default Marquee;
