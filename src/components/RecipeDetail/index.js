import axios from "axios";
import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";

function RecipeDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [recipe, setRecipe] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    console.log(`Fetching recipe with id: ${id}`);
    axios
      .get(`http://44.211.175.183:8000/recipe/${id}/`)
      .then((response) => {
        console.log("API response:", response.data);
        setRecipe(response.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Fetch error:", err);
        setLoading(false);
      });
  }, [id]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!recipe) {
    return <div>Recipe not found</div>;
  }

  const handleDelete = () => {
    axios
      .delete(`http://44.211.175.183:8000/recipe/${id}/`)
      .then(() => {
        console.log("Recipe deleted successfully");
        navigate("/"); // Redirect to home or another page
      })
      .catch((err) => {
        console.error("Delete error:", err);
      });
  };

  const handleEdit = () => {
    navigate(`/recipe/${id}/edit`);
  }

  return (
    <>
      <div className="recipe-detail">
        <h2>Title: {recipe.title}</h2>
        <p>Description: {recipe.description}</p>
      </div>
      <button className="delete-button" onClick={handleDelete}>
        Delete Recipe
      </button>
      <button className="edit-button" onClick={handleEdit}>
        Edit Recipe
      </button>
    </>
  );
}

export default RecipeDetail;
