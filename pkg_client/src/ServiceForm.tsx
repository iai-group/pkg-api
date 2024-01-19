import { useState } from "react";
import axios from "axios";
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Alert from 'react-bootstrap/Alert';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

const ServiceForm = () => {
    const [serviceName, setServiceName] = useState("");
    const [factName, setFactName] = useState("");
    const [readAccess, setReadAccess] = useState(false);
    const [writeAccess, setWriteAccess] = useState(false);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
    const baseURL = (window as any)["PKG_API_BASE_URL"] || "http://127.0.0.1:5000";

    const handleService = (isDelete: boolean) => {
        axios.post(`${baseURL}/service`, {
            serviceName, factName, readAccess,
            writeAccess, isDelete
        })
            .then((response) => {
                setError("");
                setSuccess(response.data.message);
                console.log(response.data.message);
            })
            .catch((error) => {
                setError(error.response.data.message);
                setSuccess("");
            });
    }

    const addService = () => {
        handleService(false);
    }

    const deleteService = () => {
        handleService(true);
    }

    return (
        <Form>
            <h1>Service Form</h1>
            {error && <Alert variant="danger">{error}</Alert>}
            {success && <Alert variant="success">{success}</Alert>}
            <Form.Group className="mb-6" controlId="formServiceName">
                <Form.Label>Service Name</Form.Label>
                <Form.Control required type="text" placeholder="Enter service name" onChange={(e) => setServiceName(e.target.value)} />
            </Form.Group>
            <Form.Group className="mb-6" controlId="formFactName">
                <Form.Label>Fact Name</Form.Label>
                <Form.Control required type="text" placeholder="Enter fact name" onChange={(e) => setFactName(e.target.value)} />
            </Form.Group>
            <Form.Group className="mb-6" controlId="formReadAccess">
                <Form.Check type="checkbox" label="Read Access" checked={readAccess} onChange={(e) => setReadAccess(e.target.checked)} />
            </Form.Group>
            <Form.Group className="mb-6" controlId="formWriteAccess">
                <Form.Check type="checkbox" label="Write Access" checked={writeAccess} onChange={(e) => setWriteAccess(e.target.checked)} />
            </Form.Group>
            <Row className="pt-3">
                <Col>
                    <div className="d-flex justify-content-center">
                        <Button variant="primary" onClick={addService}>
                            Add Service
                        </Button>
                        <Button variant="danger" onClick={deleteService} className="ms-2">
                            Delete Service
                        </Button>
                    </div>
                </Col>
            </Row>
        </Form>
    );
}

export default ServiceForm;
