import { useState, useContext } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import { UserContext } from "../contexts/UserContext";
import axios from "axios";
import { Alert } from "react-bootstrap";
import TripleElementFormField, {
  TripleElement,
} from "./TripleElementFormField";

const StatementPopulationForm = () => {
  const { user } = useContext(UserContext);
  const [description, setDescription] = useState("");
  const [error, setError] = useState("");
  const [info, setInfo] = useState("");
  const [subject, setSubject] = useState("");
  const [predicate, setPredicate] = useState<TripleElement>({ value: "" });
  const [object, setObject] = useState<TripleElement>({ value: "" });
  const [prefValue, setPrefValue] = useState(Number.NaN);
  const baseURL =
    (window as any)["PKG_API_BASE_URL"] || "http://127.0.0.1:5000";
  const [forceRenderKey, setForceRenderKey] = useState(Date.now());

  const resetForm = () => {
    setDescription("");
    setError("");
    setInfo("");
    setSubject("");
    setPredicate({ value: "" });
    setObject({ value: "" });
    setPrefValue(Number.NaN);
    setForceRenderKey(Date.now());
  };

  const addStatement = () => {
    if (!description) {
      setError("Please fill the required field: Description.");
      return;
    }
    // Axios sent POST request with body
    axios
      .post(`${baseURL}/statements`, {
        owner_uri: user?.uri,
        owner_username: user?.username,
        description: description,
        subject: subject,
        predicate: predicate,
        object: object,
        preference: prefValue,
      })
      .then((response) => {
        setError("");
        setInfo(response.data.message);
        resetForm();
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
          owner_uri: user?.uri,
          owner_username: user?.username,
          description: description,
          subject: subject,
          predicate: predicate,
          object: object,
          preference: prefValue,
        },
      })
      .then((response) => {
        setError("");
        setInfo(response.data.message);
        resetForm();
      })
      .catch((error) => {
        setError(error.response.data.message);
        setInfo("");
      });
  };

  return (
    <>
      {error && <Alert variant="danger">{error}</Alert>}
      {info && <Alert variant="info">{info}</Alert>}

      <Form key={forceRenderKey}>
        <Form.Group className="mb-3">
          <Form.Label>
            <b>Statement</b>
          </Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter statement description"
            required
            onChange={(e) => setDescription(e.target.value)}
          />
        </Form.Group>
        <b>Annotations</b>
        <Form.Group className="mb-3">
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
        <TripleElementFormField
          label="Predicate"
          value={predicate}
          onChange={(value) => setPredicate(value)}
        />
        <TripleElementFormField
          label="Object"
          value={object}
          onChange={(value) => setObject(value)}
        />
        <Form.Group className="mb-3">
          <Form.Label>
            <i>Preference</i>
          </Form.Label>
          <Form.Control
            type="number"
            min={-1.0}
            max={1.0}
            step={0.1}
            placeholder="Enter preference value"
            onChange={(e) => setPrefValue(parseFloat(e.target.value))}
          />
        </Form.Group>
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
    </>
  );
};

export default StatementPopulationForm;
