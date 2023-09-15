import { useState } from 'react'
import './App.css'
import Camera from './components/Camera'
import ImgUpload from './components/ImgUpload'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <h1>Welcome to SnapChef!</h1>
      <div>
        {/* <p>Click the button to open the camera</p> */}
        <Camera />
      </div>
      <div>
        <ImgUpload />
      </div>
    </>
  )
}

export default App
