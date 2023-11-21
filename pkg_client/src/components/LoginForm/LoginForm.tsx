import { useContext, useState } from "react";
import { UserContext } from "../../contexts/UserContext";
import axios from "axios";
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Alert from 'react-bootstrap/Alert';
import Row from 'react-bootstrap/Row';
import Col from "react-bootstrap/Col";

const LoginForm = () => {
    const { setUser } = useContext(UserContext);
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const baseURL = (window as any)["PKG_API_BASE_URL"] || "http://127.0.0.1:5000";

    const handleAuth = (isRegistration: boolean) => {
        axios.post(`${baseURL}/auth`, { username, password, isRegistration })
            .then((response) => {
                setUser(response.data.user);
                setError("");
                console.log(response.data.message);
            })
            .catch((error) => {
                setError(error.response.data.message);
            });
    }

    const login = () => {
        handleAuth(false);
    }

    const register = () => {
        handleAuth(true);
    }

    return (
        <Form>
            <h1>Login</h1>
            {error && <Alert variant="danger">{error}</Alert>}
            <Form.Group className="mb-6" controlId="formEmail">
                <Form.Label>Email address</Form.Label>
                <Form.Control required type="email" placeholder="Enter email" onChange={(e) => setUsername(e.target.value)} />
            </Form.Group>
            <Form.Group className="mb-6" controlId="formPassword">
                <Form.Label>Password</Form.Label>
                <Form.Control required type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} />
            </Form.Group>
            <Row className="pt-3">
                <Col>
                    <div className="d-flex justify-content-center">
                        <Button variant="primary" onClick={login}>
                            Login
                        </Button>
                        <Button variant="primary" onClick={register} className="ms-2">
                            Register
                        </Button>
                    </div>
                </Col>
            </Row>
        </Form >
    );
}

export default LoginForm;