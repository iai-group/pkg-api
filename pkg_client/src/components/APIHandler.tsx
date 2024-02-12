import React, { useContext } from "react";
import { UserContext } from "../contexts/UserContext";
import Container from "react-bootstrap/Container";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./Layout";
import NLtoPKG from "./NLtoPKG";
import PKGVisualization from "./PKGVisualization";
import PopulateForm from "./PopulateForm";

const APIHandler: React.FC = () => {
  const { user } = useContext(UserContext);

  return (
    <Container>
      <h1>Personal Knowledge Graph</h1>

      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route
              index
              element={
                <div>
                  <div>Welcome {user?.username}.</div>
                  <NLtoPKG />
                </div>
              }
            />
            <Route path="service" element={<div>Service Management</div>} />
            <Route path="population" element={<PopulateForm />} />
            <Route path="explore" element={<PKGVisualization />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </Container>
  );
};

export default APIHandler;
