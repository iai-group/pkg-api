import { useContext, useState } from "react";
import { UserContext } from "../contexts/UserContext";
import Form from 'react-bootstrap/Form';
import Button from "react-bootstrap/Button";
import axios from "axios";
import Alert from 'react-bootstrap/Alert';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Popover from 'react-bootstrap/Popover';
import { BsQuestionCircle } from "react-icons/bs";
import InputGroup from 'react-bootstrap/InputGroup';


const PopulateForm = () => {
    const { user } = useContext(UserContext);
    const [query, setQuery] = useState("");
    const [error, setError] = useState("");
    const [info, setInfo] = useState("");
    const baseURL = (window as any)["PKG_API_BASE_URL"] || "http://127.0.0.1:5000";

    const addQuery = () => {
        axios.post(`${baseURL}/population`, { owner_username: user?.username, owner_uri: user?.uri, query })
            .then((response) => {
                setError("");
                setQuery("");
                setInfo(response.data.message);
                (document.getElementById("query-field") as HTMLInputElement).value = "";
            })
            .catch((error) => {
                setError(error.response.data.message);
                setInfo("");
            });
    }

    const deleteQuery = () => {
        axios.delete(`${baseURL}/population`, { data: { owner_username: user?.username, owner_uri: user?.uri, query } })
            .then((response) => {
                setError("");
                setQuery("");
                setInfo(response.data.message);
                (document.getElementById("query-field") as HTMLInputElement).value = "";
            })
            .catch((error) => {
                setError(error.response.data.message);
                setInfo("");
            });
    }

    const popover = (
        <Popover id="popover-basic">
            <Popover.Header as="h3">Query</Popover.Header>
            <Popover.Body>
                <p>The query string should be in the following format:<br />Type: [fact|preference] Subject: [me|owner|URI] Predicate: [URI] Object: [URI|Literal] Preference: [preference]</p>
                <p>Some fields are optional, but the order must be preserved.</p>
            </Popover.Body>
        </Popover>
    );

    return (
        <Form>
            <h1>Populate PKG</h1>
            {error && <Alert variant="danger">{error}</Alert>}
            {info && <Alert variant="info">{info}</Alert>}
            <Form.Group className="mb-6" controlId="formQuery">
                <Form.Label>Query</Form.Label>
                <InputGroup className="mb-3">
                    <Form.Control id="query-field" required type="text" placeholder="Enter query" onChange={(e) => setQuery(e.target.value)} />
                    <OverlayTrigger trigger="click" placement="bottom" overlay={popover}>
                        <Button variant="light"><BsQuestionCircle /> </Button>
                    </OverlayTrigger>
                </InputGroup>
            </Form.Group>
            <Button className="mt-3" variant="primary" onClick={addQuery}>
                Add
            </Button>
            <Button className="mt-3" variant="primary" onClick={deleteQuery}>
                Delete
            </Button>
        </Form>
    )
}

export default PopulateForm;