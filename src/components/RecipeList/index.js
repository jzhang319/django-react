import React from "react";
import axios from "axios";
import { useEffect, useState } from "react";
import { NavLink } from "react-router-dom";

function RecipeList() {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios
      .get("http://44.211.175.183:8000:8000")
      .then((res) => {
        setData(res.data);
        console.log(res.data);
      })
      .catch((err) => {
        console.error(err);
      });
  }, []);

  return (
    <>
      <NavLink to="/new-recipe" className="navbar new-recipe-button">
        Add New Recipe
      </NavLink>
      {data &&
        data.map((recipe, index) => (
          <NavLink
            className="recipe-card"
            key={index}
            to={`/recipe/${recipe.id}`}
          >
            <div className="recipe-card-container">
              <h2>Title: {recipe.title}</h2>
              <p>Recipe: {recipe.description}</p>
              {/* <p>Id: {recipe.id}</p> */}
            </div>
          </NavLink>
        ))}
      <div className="recipe-spacer"></div>
    </>
  );
}

export default RecipeList;
