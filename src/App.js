import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import RecipeList from "./components/RecipeList";
import RecipeDetail from "./components/RecipeDetail";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import AddRecipeForm from "./components/AddRecipeForm";
import EditRecipeForm from "./components/EditRecipeForm";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<RecipeList />} />
        <Route path="/recipe/:id" element={<RecipeDetail />} />
        <Route path="/new-recipe" element={<AddRecipeForm />} />
        <Route path="/recipe/:id/edit" element={<EditRecipeForm />} />
      </Routes>
      <Footer />
    </Router>
  );
}

export default App;
