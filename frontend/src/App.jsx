import React, {useState} from 'react';
import axios from "axios";

function App(){
  const [image, setImage] = useState(null)
  const [colors, setColors] = useState([])

  const fileChange = (e) => {
    const file = e.target.files[0];
    setImage(file)
  };

  const handleSubmit = async () => {
    if(!image) {
      alert("Please upload image");
      return;
    }

    const formData = new FormData();
    formData.append("image", image);

    try {
      const response = await axios.post("http://localhost:8000/api/colors/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setColors(response.data.colors);
    } catch (error) {
      console.error("Error uploading image", error);
    }
  };

  return (
    <div>
      <h1>Color Finder</h1>
      <input type="file" accept='image/' onChange={fileChange} />
      <button onClick={handleSubmit} >Upload Image!</button>
      <div style={{ magingTop: "20px"}}>
        {colors.map((color, index) => (
          <div key={index} style={{ display: "inline-block", margin: "10px" }}>
            <div style={{
              backgroundColor: color.hex,
              width: "50px",
              height: "50px",
              borderRadius: "5px",
            }}></div>
            <p>{color.hex}</p>
          </div>
        ))};
      </div>
    </div>
  );
}

export default App;