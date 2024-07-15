import React from "react";
import { NavLink } from "react-router-dom";

function Navbar() {
  return (
    <>
      <NavLink to="/" className="navbar navbar-disabled">
        Welcome to Super Recipe Company
      </NavLink>
      <NavLink to="/" className="back-to-dashboard-button">
        Back to Dashboard
      </NavLink>
    </>
  );
}

export default Navbar;
