import './App.css';
import { useEffect, useState, useRef } from 'react';
import { chat, getPDFDocument } from './openRouter';
import { HumanMessage } from "langchain/schema"
import React from 'react';

interface PDFData {
  pages: Array<Page>
}

interface Page {
  metadata: Metadata
  page_content: string
}

interface Metadata {
  page: number
  source: string
}

function App() {
  const [getMessage, setGetMessage] = useState("")

  // useEffect(() => {
  //   chat.call([ new HumanMessage("What is the capital of India")]).then(data => {
  //     setGetMessage(data.content)
  //     console.log(data)
  //   })
  // }, [])

  return (
    <div className="App">
      <header className="App-header">
        <p>React + Flask Tutorial</p>
          <h3>{getMessage ? getMessage : "loading..."}</h3>
          {/* file upload that will upload to route /upload */}
          <FileUploader />

      </header>
    </div>
  );
}

const FileUploader = () => {
  const [isFileSelected, setIsFileSelected] = useState(false);
  const fileInput = useRef<HTMLInputElement | null>(null);
  const handleUpload = async (e) => {
    e.preventDefault();
    const files = fileInput?.current?.files;
    if (!files) return;
    
    // Create new FormData instance
    const formData = new FormData();
    formData.append('file', files[0]); // 'file' is the key expected in the server

    try{
      // Make the API request
      const response = await fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData
      });
      // Get the response from the server
      const data: PDFData = await response.json();
      console.log(data);
    } catch(error) {
      console.error("Error: ", error);
    }
  }

  const handleFileInputChange = () => {
    const files = fileInput?.current?.files;
    if (!files) return;
    setIsFileSelected(files.length > 0);
  }


  return (
    <form onSubmit={handleUpload}>
      <input type="file" ref={fileInput} onChange={handleFileInputChange} />
      <button disabled={!isFileSelected}  type="submit">Upload</button>
    </form>
  );
}


export default App;
