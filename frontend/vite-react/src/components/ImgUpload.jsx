import { useState } from 'react';
import axios from 'axios';

function ImgUpload() {
  const [state, setState] = useState({
    selectedImg: null,
    imgAsFile: null,
    imgResult: null,
    isAnalyzing: false,
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

    // set isAnalyzing to true while waiting for the response
    setState((prev) => ({ ...prev, isAnalyzing: true }));

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
            isAnalyzing: false, // set isAnalyzing to false after response from backend is complete
          }));
          console.log('res.data: ', res.data);
          document.querySelector("input[type='file']").value = "";
        })
        .catch((err) => {
          console.log('Error uploading and classifying the image: ', err);
          setState((prev) => ({ ...prev, isAnalyzing: false }));
        });

    };

  };


  return (

    <>
      <div>
        {state.selectedImg ? (
          <div>
            {state.isAnalyzing ? (
              <p>...Analyzing</p>
            ) : (
              // <img
              //   src={state.selectedImg}
              //   alt="Image selected"
              //   style={{ maxWidth: '200px' }} // Set a maximum width for the image
              // />
              <>
                <img
                  src={state.selectedImg}
                  alt="Image selected"
                  style={{ maxWidth: '500px', borderRadius: '10px' }} // Set a maximum width for the image
                />
                {state.imgResult && state.imgResult.class && (
                  <p>
                    Predicted Class: {state.imgResult.class}, Confidence:{" "}
                    {state.imgResult.confidence.toFixed(2)}%
                  </p>
                )}
              </>
            )}
          </div>
        ) : (
          <>
            <img
              src="https://cdn.stocksnap.io/img-thumbs/960w/cooking-food_CFBFE8F090.jpg"
              style={{ maxWidth: '500px', borderRadius: '10px' }}
            />
            <p>Select an image to upload</p>
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
      {/* <div>
        {state.imgResult && state.imgResult.error && (
          <p>{state.imgResult.error}</p>
        )}
        {state.imgResult && state.imgResult.class && (
          <p>
            Predicted Class: {state.imgResult.class}, Confidence:{" "}
            {state.imgResult.confidence.toFixed(2)}%
          </p>
        )}
      </div> */}
    </>

  );

};



export default ImgUpload;