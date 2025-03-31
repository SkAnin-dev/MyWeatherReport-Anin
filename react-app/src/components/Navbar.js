import React from 'react';

const Navbar = () => (
  <nav className="navbar is-dark" role="navigation" aria-label="main navigation">
    <div className="navbar-brand">
      <a className="navbar-item" href="/">
        My Weather Report
      </a>
      <a role="button" className="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarBasic">
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
      </a>
    </div>
    <div id="navbarBasic" className="navbar-menu">
      <div className="navbar-start">
        <a className="navbar-item" href="/">
          Home
        </a>
      </div>
      <div className="navbar-end">
        <div className="navbar-item">
          <a className="button is-light" href="/help">
            Help
          </a>
        </div>
      </div>
    </div>
  </nav>
);

export default Navbar;
