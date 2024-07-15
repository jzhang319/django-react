import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";

function EditRecipeForm() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [recipe, setRecipe] = useState({ title: "", description: "" });

  useEffect(() => {
    axios
      .get(`http://44.211.175.183:8000/recipe/${id}/`)
      .then((response) => {
        setRecipe(response.data);
      })
      .catch((error) => {
        console.error("There was an error fetching the recipe!", error);
      });
  }, [id]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setRecipe((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    axios
      .put(`http://44.211.175.183:8000/recipe/${id}/`, recipe)
      .then((response) => {
        console.log("Recipe updated successfully");
        navigate(`/recipe/${id}`);
      })
      .catch((error) => {
        console.error("There was an error updating the recipe!", error);
      });
  };

  return (
    <form onSubmit={handleSubmit} className="recipe-form">
      <div className="title-container">
        <label htmlFor="title">Title:</label>
        <input
          type="text"
          id="title"
          name="title"
          value={recipe.title}
          onChange={handleChange}
          className="title-input"
        />
      </div>
      <div className="form-group">
        <label htmlFor="description">Description:</label>
        <textarea
          id="description"
          name="description"
          value={recipe.description}
          onChange={handleChange}
          className="form-control"
        />
      </div>
      <button type="submit" className="btn btn-primary">
        Save
      </button>
    </form>
  );
}

export default EditRecipeForm;
