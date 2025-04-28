import React, { useState } from 'react';
import './App.css'; // Importing CSS file for styling

function App() {
  const [images, setImages] = useState([]);

  const handleImageUpload = (index, event) => {
    const files = event.target.files;
    if (files.length > 0) {
      const reader = new FileReader();
      reader.onload = () => {
        const newImage = reader.result;
        const updatedImages = [...images];
        updatedImages[index] = newImage;
        setImages(updatedImages);
      };
      reader.readAsDataURL(files[0]);
    }
  };

  const handleSubmit = () => {
    // Logic for handling form submission goes here
    console.log("Form submitted with images:", images);
  };

  return (
    <div>
      <h1>Face Similarity Detection AI</h1>
      <h3>Upload 3 images - AI will determine which is closer to the Anchor Image</h3>
      <div className="drop-zone-container">
        {[{ text: 'Upload Anchor Image' }, { text: 'Upload Image 1' }, { text: 'Upload Image 2' }].map((item, index) => (
          <div key={index} className="drop-zone">
            <input type="file" accept="image/*" onChange={(event) => handleImageUpload(index, event)} />
            {images[index] && <img src={images[index]} alt={`Image ${index}`} />}
            {!images[index] && (
              <p>{item.text}</p>
            )}
          </div>
        ))}
      </div>
      <button className="submit-button" onClick={handleSubmit}>Submit</button>
      <div className="result-block">
          <h2>Results</h2>
          <p>Image i is more similar to the Anchor Image</p>
      </div>
    </div>
  );
}

export default App;





