// Natural language to PKG component

import { Container } from "react-bootstrap";
import { UserContext } from "../contexts/UserContext";
import { useContext, useState } from "react";
import axios from "axios";
import QueryForm from "./QueryForm";

const NLtoPKG = () => {
  const { user } = useContext(UserContext);
  const [error, setError] = useState("");
  const baseURL =
    (window as any)["PKG_API_BASE_URL"] || "http://127.0.0.1:5000";

  const handleSubmit = (query: string) => {
    return axios
      .post(`${baseURL}/nl`, {
        query: query,
        username: user?.username,
        user_uri: user?.uri,
      })
      .then((response) => {
        // TODO: Handle response.
        // Output can be displayed in information-container.
        setError("");
      })
      .catch((error) => {
        setError(error.message);
        throw error;
      });
  };

  return (
    <Container>
      <div>
        <b>Manage your PKG with natural language queries.</b>
      </div>
      <QueryForm handleSubmit={handleSubmit} error={error} />
      <Container id="information-container"></Container>
    </Container>
  );
};

export default NLtoPKG;
