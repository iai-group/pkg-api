import React, { useContext } from "react";
import "./App.css";
import APIHandler from "./components/APIHandler";
import LoginForm from "./components/LoginForm";
<<<<<<< HEAD
=======
import ServiceForm from "./components/ServiceForm";
>>>>>>> Service management frontend and backedn
import Container from 'react-bootstrap/Container'
import { UserContext } from "./contexts/UserContext";

function App() {
  const { user } = useContext(UserContext);

<<<<<<< HEAD
  const content = user ? <APIHandler /> : <LoginForm />;
=======
  const content = user ? <APIHandler /> : <ServiceForm />;
>>>>>>> Service management frontend and backedn

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
