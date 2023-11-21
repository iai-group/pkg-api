import React, { useContext } from "react";
import "./App.css";
import APIHandler from "./APIHandler";
import LoginForm from "./components/LoginForm/LoginForm";
import Container from 'react-bootstrap/Container'
import { UserContext } from "./contexts/UserContext";

function App() {
  const { user } = useContext(UserContext);

  const content = !user ? <LoginForm /> : <APIHandler />;

  return (
    <Container className="p-3">
      <Container className="p-3 mb-4 bg-light rounded-3">
        <div className="App">
          {content}
        </div>
      </Container>
    </Container>
  );
}

export default App;
