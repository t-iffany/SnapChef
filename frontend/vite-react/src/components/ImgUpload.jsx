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
                  style={{ maxWidth: '400px' }} // Set a maximum width for the image
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
              src="data:image/jpeg;base64,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"
              style={{ maxWidth: '400px' }}
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