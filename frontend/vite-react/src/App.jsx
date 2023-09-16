import { useState } from 'react'
import './App.css'
import Camera from './components/Camera'
import ImgUpload from './components/ImgUpload'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <h1>Welcome to SnapChef! 
        <img 
          src="https://img.icons8.com/color/96/soup-plate.png"
          style={{ marginBottom: '-12px' }}
        />
      </h1>

      <div>
        <ImgUpload />
      </div>

      <div style ={{ marginTop: '50px' }}>
        <Camera />
      </div>
    </>
  )
}

export default App
