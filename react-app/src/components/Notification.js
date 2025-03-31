import React from 'react';

const Notification = ({ type, message, onClose }) => (
  <div className={`notification is-${type}`} style={{ marginTop: '20px' }}>
    <button className="delete" onClick={onClose}></button>
    {message}
  </div>
);

export default Notification;
