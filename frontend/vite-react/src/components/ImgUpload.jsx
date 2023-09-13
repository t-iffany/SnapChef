import { useState } from 'react';
import axios from 'axios';

function ImgUpload() {
  const [state, setState] = useState({
    selectedImg: null,
    imgAsFile: null,
    imgResult: null,
  })

  const handleFileSelect = (event) => {
    console.log(event.target.files[0])

    setState({
      selectedImg: URL.createObjectURL(event.target.files[0]),
      imgAsFile: event.target.files[0]
    });
  };

  const handleUpload = (event) => {
    event.preventDefault();

    const reader = new FileReader();
    reader.readAsDataURL(state.imgAsFile)

    reader.onload = () => {
      const base64Img = reader.result;

      axios
        .post("http://127.0.0.1:5000/", 
        JSON.stringify(base64Image)
        , {
            headers: {
                "Content-Type": "application/json; charset=UTF-8",
            },
        })
        .then((res) => {
            console.log('res', res)
            setState(prev => ({ ...prev, imageResult: res.data }))
            document.querySelector("input[type='file']").value = "";
            state.submitted(true);
        })
        .catch((err) => {
            console.log(err);
        });

    }

  }

  return (
    
    <>
      <div>
        <form onSubmit={handleUpload}>
          <input
            id="inputTag"
            className="choose-image"
            type="file"
            name="image"
            onChange={handleFileSelect}
            accept="image/*"
          />
        </form>
        <button 
          type="button"
          onClick={handleUpload}
        >
          Upload
        </button>
      </div>
      {state.imgResult}
    </>

  )

};



export default ImgUpload;