import React, { useEffect } from 'react';

const Hero = () => {
  useEffect(() => {
    const greetingBox = document.getElementById("welcome");
    if (greetingBox) {
      greetingBox.innerHTML = " (Welcome User!) ";
    }
  }, []);
  return (
    <section className="hero is-primary">
      <div className="hero-body">
        <div className="container">
          <h1 className="title" style={{ fontWeight: 500 }}>
            My Weather Report <span id="welcome">(Unknown User)</span>
          </h1>
        </div>
      </div>
    </section>
  );
};

export default Hero;
