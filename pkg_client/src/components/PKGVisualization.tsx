// Natural language to PKG component

import { Container } from "react-bootstrap";
import { UserContext } from "../contexts/UserContext";
import { useContext, useEffect, useState } from "react";
import axios from "axios";
import QueryForm from "./QueryForm";
import Button from "react-bootstrap/Button";

const PKGVisualization = () => {
  const { user } = useContext(UserContext);
  const [error, setError] = useState("");
  const [image_path, setImagePath] = useState("");
  const [query_info, setQueryInfo] = useState("");
  const [result, setResult] = useState("");
  const baseURL =
    (window as any)["PKG_API_BASE_URL"] || "http://127.0.0.1:5000";

  useEffect(() => {
    getImage();
  }, []);

  // TODO: export this function to reuse it in other components
  const getImage = () => {
    axios
      .get(`${baseURL}/explore`, {
        params: {
          owner_username: user?.username,
          owner_uri: user?.uri,
        },
        responseType: "blob",
      })
      .then((response) => {
        setError("");
        const imageURL = URL.createObjectURL(
          new Blob([response.data], {
            type: "image/png",
          })
        );
        setImagePath(imageURL);
      })
      .catch((error) => {
        setError(error.message);
        throw error;
      });
  };

  const executeQuery = (query: string) => {
    return axios
      .post(`${baseURL}/explore`, {
        sparql_query: query,
        owner_username: user?.username,
        owner_uri: user?.uri,
      })
      .then((response) => {
        setError("");
        console.log(response.data);
        setQueryInfo(response.data.message);
        setResult(response.data.result);
      })
      .catch((error) => {
        setError(error.message);
        throw error;
      });
  };

  return (
    <Container>
      <div>
        <b>Here you can execute your own SPARQL queries to manage your PKG.</b>
      </div>
      <QueryForm handleSubmit={executeQuery} error={error} />
      <div>Query execution status: {query_info}</div>
      <div>Query execution result: {result}</div>
      <div>
        <b>This is your current PKG:</b>
      </div>
      <img src={image_path} alt="PKG" style={{ width: "100%" }} />
    </Container>
  );
};

export default PKGVisualization;
