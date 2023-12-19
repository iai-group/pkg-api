import { useContext, useState } from "react";
import { UserContext } from "../contexts/UserContext";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import Alert from "react-bootstrap/Alert";
import Container from "react-bootstrap/esm/Container";
import axios from "axios";

const PopulateForm = () => {
  const { user } = useContext(UserContext);
  const [subjectURI, setSubjectURI] = useState("");
  const [predicateURI, setPredicateURI] = useState("");
  const [objectURI, setObjectURI] = useState("");
  const [preference, setPreference] = useState(0.0);
  const [error, setError] = useState("");
  const [info, setInfo] = useState("");
  const baseURL =
    (window as any)["PKG_API_BASE_URL"] || "http://127.0.0.1:5000";

  const addFact = () => {
    if (!subjectURI || !predicateURI || !objectURI) {
      setError(
        "Please fill in the fields: Subject URI, Predicate URI, and Object URI."
      );
      return;
    }
    // Axios sent POST request with body
    axios
      .post(`${baseURL}/facts`, {
        subjectURI: subjectURI,
        predicate: predicateURI,
        objectURI: objectURI,
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

  const deleteFact = () => {
    if (!subjectURI || !predicateURI || !objectURI) {
      setError(
        "Please fill in the fields: Subject URI, Predicate URI, and Object URI."
      );
      return;
    }
    // Axios send DELETE request with body
    axios
      .delete(`${baseURL}/facts`, {
        data: {
          subjectURI: subjectURI,
          predicate: predicateURI,
          objectURI: objectURI,
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

  const addPreference = () => {
    if (!subjectURI || !objectURI || !preference) {
      setError(
        "Please fill in the fields: Subject URI, Object URI, and preference."
      );
      return;
    }
    // Axios sent POST request with body
    axios
      .post(`${baseURL}/preferences`, {
        subjectURI: subjectURI,
        objectURI: objectURI,
        preference: preference,
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
      <Form>
        <p>
          Complete the following form to either add a preference or add/remove a
          fact.
        </p>
        {error && <Alert variant="danger">{error}</Alert>}
        {info && <Alert variant="info">{info}</Alert>}
        <Form.Group className="mb-3" controlId="formSubject">
          <Form.Label>
            <b>Subject URI</b>
          </Form.Label>
          <Form.Check
            type="switch"
            id="custom-switch"
            label="Me"
            onChange={(e) => {
              if (e.target.checked) {
                setSubjectURI(user?.uri || "");
                // Disable the input
                (
                  document.getElementById("inputSubjectURI") as HTMLInputElement
                ).disabled = true;
                document
                  .getElementById("inputSubjectURI")
                  ?.setAttribute("placeholder", user?.uri || "");
              } else {
                setSubjectURI("");
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
            placeholder="Enter subject URI"
            id="inputSubjectURI"
            onChange={(e) => setSubjectURI(e.target.value)}
          />
        </Form.Group>
        <Form.Group className="mb-3" controlId="formPredicate">
          <Form.Label>
            <b>Predicate URI</b>
          </Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter predicate URI"
            onChange={(e) => setPredicateURI(e.target.value)}
          />
          <Form.Text className="text-muted">
            Predicate URI is not required when adding a new preference.
          </Form.Text>
        </Form.Group>
        <Form.Group className="mb-3" controlId="formObject">
          <Form.Label>
            <b>Object URI</b>
          </Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter object URI"
            onChange={(e) => setObjectURI(e.target.value)}
          />
        </Form.Group>
        <Form.Group className="mb-3" controlId="formPreference">
          <Form.Label>
            <b>Preference</b>
          </Form.Label>
          <Form.Control
            type="number"
            placeholder="Enter preference"
            defaultValue={preference}
            onChange={(e) => setPreference(parseFloat(e.target.value))}
          />
          <Form.Text className="text-muted">
            Preference is not required when adding or removing a new fact.
          </Form.Text>
        </Form.Group>
        {/* TODO: Add section to manage access rights of services
        See issue: https://github.com/iai-group/pkg-api/issues/66 */}
        <Button
          className="mt-3"
          style={{ marginRight: "10px" }}
          variant="primary"
          onClick={addFact}
        >
          Add fact
        </Button>
        <Button
          className="mt-3"
          style={{ marginRight: "10px" }}
          variant="primary"
          onClick={deleteFact}
        >
          Delete fact
        </Button>
        <Button className="mt-3" variant="primary" onClick={addPreference}>
          Add preference
        </Button>
      </Form>
    </Container>
  );
};

export default PopulateForm;
