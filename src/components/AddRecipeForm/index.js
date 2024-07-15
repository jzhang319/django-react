import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom"; // Import useNavigate

const AddRecipeForm = () => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate(); // Initialize navigate

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://44.211.175.183:8000:8000", {
        title,
        description,
      });
      console.log("Recipe added:", response.data);
      // Optionally, reset the form or redirect the user
      setTitle("");
      setDescription("");
      navigate("/"); // Redirect to home page
    } catch (err) {
      console.error("Error adding recipe:", err);
      setError("Failed to add recipe. Please try again.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="recipe-form">
      <div className="form-group">
        <label>Title:</label>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
          className="form-input"
        />
      </div>
      <div className="form-group">
        <label>Description:</label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          required
          className="form-textarea"
        />
      </div>
      {error && <p className="error-message">{error}</p>}
      <button type="submit" className="form-button">
        Add Recipe
      </button>
    </form>
  );
};

export default AddRecipeForm;
