import React, { useState } from 'react';

const CaptureButton = () => {

  const handleClick = () => {
    // Implement logic to send a request to the Flask backend
    // Use fetch or Axios to make the API call
    // For example, can use fetch like this:
    fetch('http://localhost:5000/capture-image', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      // data we want to send to the Flask backend
      body: JSON.stringify({ key: 'value' }),
    })
      .then((response) => response.json())
      .then((data) => {
        // Handle the response from your backend here
        console.log(data);
      })
      .catch((error) => {
        // Handle any errors here
        console.error('Error:', error);
      });
  };

  return (
    <div>
      <button onClick={handleClick}>Capture</button>
    </div>
  );
};

export default CaptureButton;
