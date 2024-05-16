import { BrowserRouter, Route, Routes } from "react-router-dom";
import React, { useContext } from "react";

import Container from "react-bootstrap/Container";
import Layout from "./Layout";
import { UserContext } from "../contexts/UserContext";

const APIHandler: React.FC = () => {
  const { user } = useContext(UserContext);

  return (
    <Container>
      <h1>Personal Knowledge Graph</h1>

      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<div>Welcome {user?.username}</div>} />
            {/* <Route path="service" element={<div>Service Management</div>} /> */}
            <Route path="population" element={<div>PKG Population</div>} />
            <Route path="explore" element={<div>PKG Exploration</div>} />
          </Route>
        </Routes>
      </BrowserRouter>
    </Container>
  );
};

export default APIHandler;
