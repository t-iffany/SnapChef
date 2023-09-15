import { useState } from 'react';
import axios from 'axios';

function ImgUpload() {
  const [state, setState] = useState({
    selectedImg: null,
    imgAsFile: null,
    imgResult: null,
  });

  const handleFileSelect = (event) => {
    console.log(event.target.files[0]);

    setState({
      selectedImg: URL.createObjectURL(event.target.files[0]),
      imgAsFile: event.target.files[0],
      imgResult: null, // clear previous results when a new image is selected
    });
  };

  const handleUpload = (event) => {
    event.preventDefault();

    // check if an image is selected
    if (!state.imgAsFile) {
      console.log('Please select an image');
      return;
    }

    const reader = new FileReader();
    reader.readAsDataURL(state.imgAsFile);

    reader.onload = () => {
      const base64Image = reader.result;

      axios
        .post("http://127.0.0.1:5000/classify-image", JSON.stringify(base64Image), {
          headers: {
            "Content-Type": "application/json; charset=UTF-8",
          },
        })
        .then((res) => {
          console.log('res', res);
          setState((prev) => ({ 
            ...prev, 
            imgResult: {
              class: res.data.class,
              confidence: res.data.confidence,
            },
          }));
          console.log('res.data: ', res.data);
          document.querySelector("input[type='file']").value = "";
          // state.submitted(true);
        })
        .catch((err) => {
          console.log('Error uploading and classifying the image: ', err);
        });

    };

  };


  return (

    <>
      <div>
        {state.selectedImg ? (
          <img
            src={state.selectedImg}
            alt="Image selected"
          />
        ) : (
          <>
            <p>Select an image</p>
          </>
        )}
      </div>

      <form>
        <input
          id="inputTag"
          className="choose-image"
          type="file"
          name="image"
          onChange={handleFileSelect}
          accept="image/*"
        />
        <button
          type="button"
          onClick={handleUpload}
        >
          Upload
        </button>
      </form>
      <div>
        {state.imgResult && state.imgResult.error && (
          <p>{state.imgResult.error}</p>
        )}
        {state.imgResult && state.imgResult.class && (
          <p>
            Predicted Class: {state.imgResult.class}, Confidence:{" "}
            {state.imgResult.confidence.toFixed(2)}%
          </p>
        )}
      </div>
    </>

  );

};



export default ImgUpload;