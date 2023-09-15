import React, { useState, useRef } from 'react';

function Camera() {
  // create state variables to store the camera stream and captured image data
  const [cameraStream, setCameraStream] = useState(null);
  const [capturedImage, setCapturedImage] = useState(null);

  const videoRef = useRef();

  // access the user's camera using the navigator method
  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      console.log('Camera Stream:', stream);
      setCameraStream(stream);
      videoRef.current.srcObject = stream; // Assign the stream to the video element
    } catch (error) {
      console.error('Error accessing camera:', error);
    }
  };

  // use canvas element to draw the current video frame onto it and convert it to an image
  const captureImage = () => {
    if (cameraStream) {
      const videoElement = videoRef.current;
      const canvas = document.createElement('canvas');
      canvas.width = videoElement.videoWidth;
      canvas.height = videoElement.videoHeight;
      canvas.getContext('2d').drawImage(videoElement, 0, 0);

      // Convert the canvas to a data URL representing the captured image
      const imageDataUrl = canvas.toDataURL('image/png');
      setCapturedImage(imageDataUrl);

      // Stop the camera stream
      cameraStream.getTracks().forEach((track) => track.stop());
    }
  };

  // render the component
  return (
    <div>
      {cameraStream ? (
        <>
          <video ref={videoRef} autoPlay playsInline style={{ width: '100%', height: 'auto' }} />
          <button onClick={captureImage}>Capture</button>
        </>
      ) : (
        <button onClick={startCamera}>Start Camera</button>
      )}
      {capturedImage && <img src={capturedImage} alt="Captured" />}
    </div>
  );
}

export default Camera;
