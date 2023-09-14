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

    // try {
    //   const formData = new FormData();
    //   formData.append('image', state.imgAsFile);

    //   // // Extract file extension from the selected file
    //   // const fileExtension = state.imgAsFile.name.split('.').pop().toLowerCase();

    //   // // Include the file extension when sending data
    //   // const formData = new FormData();
    //   // formData.append('image', state.imgAsFile);
    //   // formData.append('extension', fileExtension);


    //   // send the image to the backend for classification
    //   const response = await axios.post('http://127.0.0.1:5000/classify-image', formData, {
    //     headers: {
    //       'Content-Type': 'multipart/form-data', // Set the content type to multipart/form-data
    //     },
    //   });

    //   console.log("response: ", response);
    //   // Check if the response contains the expected data
    //   if (response.data && response.data.predicted_class && response.data.confidence) {
    //     // handle the response from the backend
    //     const { predicted_class, confidence } = response.data;

    //     setState((prev) => ({
    //       ...prev,
    //       imgResult: `Predicted Class: ${predicted_class}, Confidence: ${confidence.toFixed(2)}`,
    //     }));
    //   } else {
    //     console.error('Invalid response format from the backend:', response.data);
    //   }
    // } catch (error) {
    //   console.error('Error uploading and classifying the image:', error);

    //   // display error message from the response directly
    //   setState((prev) => ({
    //     ...prev,
    //     imgResult: 'Error from the backend: ${response.data}',
    //   }));
    // }



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
          setState((prev) => ({ ...prev, imgResult: res.data }));
          console.log('res.data: ', res.data);
          document.querySelector("input[type='file']").value = "";
          // state.submitted(true);
        })
        .catch((err) => {
          console.log('Error uploading and classifying the image: ', err);
        });

      // reader.readAsDataURL(state.imgAsFile);

    };

  };

  // const reader = new FileReader();
  // reader.readAsDataURL(state.imgAsFile);

  // reader.onload = (e) => {
  //   const base64Image = e.target.result;

  //   axios
  //       .post("http://127.0.0.1:5000/classify-image",
  //       JSON.stringify(base64Image)
  //       , {
  //         headers: {
  //           "Content-Type": "application/json; charset=UTF-8",
  //         },
  //       })
  //       .then((res) => {
  //         console.log('res', res);
  //         setState(prev => ({ ...prev, imageResult: res.data }));
  //         document.querySelector("input[type='file']").value = "";
  //         state.submitted(true);
  //       })
  //       .catch((err) => {
  //           console.log('Error uploading and classifying the image: ', err);
  //       });

  //     // reader.readAsDataURL(state.imgAsFile);

  //   console.log('e.target.result: ', e.target.result);
  //   console.log('imgAsFile: ', imgAsFile);
  //   console.log('JSON.stringify(base64Image): ', JSON.stringify(base64Image))

  // };


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

      {/* <form onSubmit={handleUpload}> */}
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
        {state.imgResult && state.imgResult.predicted_class && (
          <p>
            Predicted Class: {state.imgResult.predicted_class}, Confidence:{" "}
            {state.imgResult.confidence.toFixed(2)}%
          </p>
        )}
      </div>
    </>

  );

};



export default ImgUpload;