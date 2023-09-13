import { useState } from 'react'
import './App.css'
import Camera from './components/Camera'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <h1>Welcome to SnapChef!</h1>
      <div className="container">
        <p>Click the button to open the camera</p>
        <Camera />
      </div>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
