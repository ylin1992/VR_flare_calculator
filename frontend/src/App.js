import React, {useState, useEffect} from 'react'
import Upload from './Upload';
import UploadMulti from './UploadMulti';
function App() {

  const [data, setData] = useState({});

  useEffect( () => {
    fetch("http://localhost:5000").then(
      res => res.json()
    ).then(
      data => {
        console.log(data)
        setData(data)
      }
    )
  }, [])

  return (
    <div>
      <h1>{data.this}</h1>
      <Upload />
      <UploadMulti />
    </div>
  )
}

export default App
