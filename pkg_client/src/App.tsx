import React, { useContext } from "react";
import "./App.css";
import APIHandler from "./components/APIHandler";
import LoginForm from "./components/LoginForm";
import Container from "react-bootstrap/Container";
import { UserContext } from "./contexts/UserContext";

function App() {
  const { user } = useContext(UserContext);

  const content = user ? <APIHandler /> : <LoginForm />;

  return (
    <Container className="p-3">
      <Container className="p-3 mb-4 bg-light rounded-3">
        <div className="App">{content}</div>
      </Container>
    </Container>
  );
}

export default App;
