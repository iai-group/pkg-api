// Natural language to PKG component

import { Container } from "react-bootstrap";
import { UserContext } from "../contexts/UserContext";
import { useContext, useState } from "react";
import axios from "axios";
import QueryForm from "./QueryForm";
import Button from 'react-bootstrap/Button';

const PKGVisualization = () => {
    const { user } = useContext(UserContext);
    const [error, setError] = useState("");
    const [image_path, setImagePath] = useState("");
    const [image_info, setImageInfo] = useState("");
    const [query_info, setQueryInfo] = useState("");
    const [result, setResult] = useState("");
    const baseURL =
        (window as any)["PKG_API_BASE_URL"] || "http://127.0.0.1:5000";

    const getImagePath = () => {
        axios.get(`${baseURL}/explore`, {})
            .then((response) => {
                setError("");
                console.log(response.data.message);
                setImageInfo(response.data.message);
                setImagePath(response.data.img_path);
            })
            .catch((error) => {
                setError(error.message);
                throw error;
            });
    };

    const executeQuery = (query: string) => {
        return axios
            .post(`${baseURL}/explore`, {
                query: query,
                username: user?.username,
                user_uri: user?.uri,
            })
            .then((response) => {
                setError("");
                console.log(response.data.message);
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
                <div>{image_info}</div>
            </div>
            <QueryForm handleSubmit={executeQuery} error={error} />
            <div>Query execution status: {query_info}</div>
            <div>Query execution result: {result}</div>
            <div>
                <b>This is your current PKG:</b>
            </div>
            <div>[Only for testing] Local path to the image: {image_path}</div>
            <img src={image_path} alt="PKG" />
        </Container>
    );

};

export default PKGVisualization;