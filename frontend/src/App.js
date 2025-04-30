import React, { useState, useRef } from 'react';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const fileInput = useRef();

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    setFile(selected);
    setResult(null);
    setError("");
    if (selected) {
      setPreview(URL.createObjectURL(selected));
    } else {
      setPreview(null);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const dropped = e.dataTransfer.files[0];
    setFile(dropped);
    setResult(null);
    setError("");
    if (dropped) {
      setPreview(URL.createObjectURL(dropped));
    } else {
      setPreview(null);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setResult(null);
    setError("");
    const formData = new FormData();
    formData.append('file', file);
    try {
      const response = await fetch('http://localhost:8000/predict/', {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) throw new Error('Prediction failed');
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <header className="header">
        <img src="https://img.icons8.com/color/96/animal.png" alt="WildShapes Logo" className="logo" />
        <h1>WildShapes</h1>
        <p className="subtitle">Animal & Shape Classifier</p>
      </header>
      <div
        className={`dropzone${file ? ' has-file' : ''}`}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onClick={() => fileInput.current.click()}
      >
        {preview ? (
          <img src={preview} alt="Preview" className="preview" />
        ) : (
          <span>Drag & drop an image here, or click to select</span>
        )}
        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          ref={fileInput}
          style={{ display: 'none' }}
        />
      </div>
      <button onClick={handleUpload} disabled={!file || loading} className="upload-btn">
        {loading ? 'Classifying...' : 'Classify'}
      </button>
      {result && (
        <div className="result-card">
          <h2>Prediction Result</h2>
          <div className="predicted-class">{result.class}</div>
          <div className="confidence-bar-outer">
            <div
              className="confidence-bar-inner"
              style={{ width: `${result.confidence * 100}%` }}
            ></div>
          </div>
          <div className="confidence-label">
            Confidence: {(result.confidence * 100).toFixed(1)}%
          </div>
          <div className="fun-fact">
            <span role="img" aria-label="lightbulb">💡</span> {result.fact}
          </div>
        </div>
      )}
      {error && <div className="error">{error}</div>}
      <footer className="footer">
        <p>Made with <span role="img" aria-label="heart">❤️</span> for CAI2840C | <a href="https://icons8.com/icon/114496/animal" target="_blank" rel="noopener noreferrer">Icon</a></p>
      </footer>
    </div>
  );
}

export default App;
