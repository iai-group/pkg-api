import { useContext, useState } from "react";
import { UserContext } from "../contexts/UserContext";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import Alert from "react-bootstrap/Alert";
import Container from "react-bootstrap/esm/Container";
import axios from "axios";
import Col from "react-bootstrap/esm/Col";
import Row from "react-bootstrap/esm/Row";

const PopulateForm = () => {
  const { user } = useContext(UserContext);
  const [description, setDescription] = useState("");
  const [subject, setSubject] = useState("");
  const [predicate, setPredicate] = useState("");
  const [object, setObject] = useState("");
  const [preference, setPreference] = useState(0.0);
  const [prefTopic, setPrefTopic] = useState("");
  const [error, setError] = useState("");
  const [info, setInfo] = useState("");
  const baseURL =
    (window as any)["PKG_API_BASE_URL"] || "http://127.0.0.1:5000";

  const addStatement = () => {
    if (!description) {
      setError("Please fill the required field: Description.");
      return;
    }
    // Axios sent POST request with body
    axios
      .post(`${baseURL}/statements`, {
        description: description,
        subject: subject,
        predicate: predicate,
        object: object,
        preference: preference,
        prefTopic: prefTopic,
      })
      .then((response) => {
        setError("");
        setInfo(response.data.message);
      })
      .catch((error) => {
        setError(error.response.data.message);
        setInfo("");
      });
  };

  const deleteStatement = () => {
    if (!description) {
      setError("Please fill the required field: Description.");
      return;
    }
    // Axios send DELETE request with body
    axios
      .delete(`${baseURL}/statements`, {
        data: {
          description: description,
          subject: subject,
          predicate: predicate,
          object: object,
          preference: preference,
          prefTopic: prefTopic,
        },
      })
      .then((response) => {
        setError("");
        setInfo(response.data.message);
      })
      .catch((error) => {
        setError(error.response.data.message);
        setInfo("");
      });
  };

  return (
    <Container>
      <p>
        Complete the following form to either add or delete a statement.{" "}
        <b>
          It is assumed that you are familiar with the{" "}
          <a href="https://iai-group.github.io/pkg-vocabulary/" target="blank">
            PKG vocabulary
          </a>
          .
        </b>
      </p>
      <p>
        The annotation fields may be filled with either an URI or the
        representation of a blank node. For example:
      </p>
      <ul>
        <li>
          the predicate <i>hasName</i> may be represented as{" "}
          <i>http://xmlns.com/foaf/0.1/name</i> or <i>foaf:name</i>
        </li>
        <li>
          the predicate <i>dislike</i> may be represented as blank node{" "}
          <i>[ a skos:Concept ; dc:description "dislike" ]</i>
        </li>
      </ul>

      <Form>
        {error && <Alert variant="danger">{error}</Alert>}
        {info && <Alert variant="info">{info}</Alert>}
        <Form.Group className="mb-3" controlId="formDescription">
          <Form.Label>
            <b>Description</b>
          </Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter statement description"
            required
            onChange={(e) => setDescription(e.target.value)}
          />
        </Form.Group>
        <b>Annotations</b>
        <Form.Group className="mb-3" controlId="formSubject">
          <Form.Label>
            <i>Subject</i>
          </Form.Label>
          <Form.Check
            type="switch"
            id="custom-switch"
            label="Me"
            onChange={(e) => {
              if (e.target.checked) {
                setSubject(user?.uri || "");
                // Disable the input
                (
                  document.getElementById("inputSubjectURI") as HTMLInputElement
                ).disabled = true;
                document
                  .getElementById("inputSubjectURI")
                  ?.setAttribute("placeholder", user?.uri || "");
              } else {
                setSubject("");
                // Enable the input
                (
                  document.getElementById("inputSubjectURI") as HTMLInputElement
                ).disabled = false;
                document
                  .getElementById("inputSubjectURI")
                  ?.setAttribute("placeholder", "Enter subject URI");
              }
            }}
          />
          <Form.Control
            type="text"
            id="inputSubjectURI"
            onChange={(e) => setSubject(e.target.value)}
          />
        </Form.Group>
        <Form.Group className="mb-3" controlId="formPredicate">
          <Form.Label>
            <i>Predicate</i>
          </Form.Label>
          <Form.Control
            type="text"
            onChange={(e) => setPredicate(e.target.value)}
          />
        </Form.Group>
        <Form.Group className="mb-3" controlId="formObject">
          <Form.Label>
            <i>Object</i>
          </Form.Label>
          <Form.Control
            type="text"
            onChange={(e) => setObject(e.target.value)}
          />
        </Form.Group>
        <Form.Group className="mb-3" controlId="formPreference">
          <Form.Label>
            <i>Preference</i>
          </Form.Label>
          <Row className="mb-3">
            <Col sm={5}>
              <Form.Control
                type="text"
                placeholder="Enter topic"
                onChange={(e) => setPrefTopic(e.target.value)}
              />
            </Col>
            <Col sm={1}>
              <Form.Control
                type="number"
                min="-1.0"
                max="1.0"
                step="0.1"
                placeholder="Enter preference"
                defaultValue={preference}
                onChange={(e) => setPreference(parseFloat(e.target.value))}
              />
            </Col>
          </Row>
        </Form.Group>
        {/* TODO: Add section to manage access rights of services
        See issue: https://github.com/iai-group/pkg-api/issues/66 */}
        <Button
          className="mt-3"
          style={{ marginRight: "10px" }}
          variant="primary"
          onClick={addStatement}
        >
          Add statement
        </Button>
        <Button
          className="mt-3"
          style={{ marginRight: "10px" }}
          variant="primary"
          onClick={deleteStatement}
        >
          Delete statement
        </Button>
      </Form>
    </Container>
  );
};

export default PopulateForm;
