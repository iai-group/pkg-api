import { useState, useContext } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import { UserContext } from "../contexts/UserContext";
import { TripleElement } from "./PopulateForm";
import axios from "axios";
import { Alert } from "react-bootstrap";

const StatementPopulationForm = () => {
  const { user } = useContext(UserContext);
  const [description, setDescription] = useState("");
  const [error, setError] = useState("");
  const [info, setInfo] = useState("");
  const [subject, setSubject] = useState("");
  const [predicate, setPredicate] = useState<TripleElement>({
    value: "",
  });
  const [predicateSwitch, setPredicateSwitch] = useState(false);
  const [object, setObject] = useState<TripleElement>({
    value: "",
  });
  const [objectSwitch, setObjectSwitch] = useState(false);
  const [prefValue, setPrefValue] = useState(Number.NaN);
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
        preference: prefValue,
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
          preference: prefValue,
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
    <>
      {error && <Alert variant="danger">{error}</Alert>}
      {info && <Alert variant="info">{info}</Alert>}

      <Form>
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
        <Form.Group className="mb-3">
          <Form.Label>
            <i>Predicate</i>
          </Form.Label>
          <Form.Check
            type="switch"
            label="Concept"
            id="predicate-switch"
            checked={predicateSwitch}
            onChange={(e) => {
              setPredicateSwitch(e.target.checked);
            }}
          />
          {!predicateSwitch && (
            <Form.Control
              type="text"
              onChange={(e) => setPredicate({ value: e.target.value })}
            />
          )}
          {predicateSwitch && (
            <>
              <Form.Control
                type="text"
                placeholder="Enter concept description"
                id="predicate-description"
                onChange={(e) => {
                  typeof predicate.value === "string"
                    ? setPredicate({
                        value: {
                          description: e.target.value,
                          related: [],
                          broader: [],
                          narrower: [],
                        },
                      })
                    : setPredicate({
                        value: {
                          description: e.target.value,
                          related: predicate?.value?.related || [],
                          broader: predicate?.value?.broader || [],
                          narrower: predicate?.value?.narrower || [],
                        },
                      });
                }}
              />
              <Form.Control
                type="text"
                placeholder="Enter concept related entities"
                id="predicate-related"
                onChange={(e) => {
                  typeof predicate.value === "string"
                    ? setPredicate({
                        value: {
                          description: e.target.value,
                          related: [],
                          broader: [],
                          narrower: [],
                        },
                      })
                    : setPredicate({
                        value: {
                          description: predicate?.value?.description || "",
                          related: e.target.value.split(","),
                          broader: predicate?.value?.broader || [],
                          narrower: predicate?.value?.narrower || [],
                        },
                      });
                }}
              />
              <Form.Control
                type="text"
                placeholder="Enter concept broader entities"
                id="predicate-broader"
                onChange={(e) => {
                  typeof predicate.value === "string"
                    ? setPredicate({
                        value: {
                          description: "",
                          related: [],
                          broader: e.target.value.split(","),
                          narrower: [],
                        },
                      })
                    : setPredicate({
                        value: {
                          description: predicate?.value?.description || "",
                          related: predicate?.value?.related || [],
                          broader: e.target.value.split(","),
                          narrower: predicate?.value?.narrower || [],
                        },
                      });
                }}
              />
              <Form.Control
                type="text"
                placeholder="Enter concept narrower entities"
                id="predicate-narrower"
                onChange={(e) => {
                  typeof predicate.value === "string"
                    ? setPredicate({
                        value: {
                          description: "",
                          related: [],
                          broader: [],
                          narrower: e.target.value.split(","),
                        },
                      })
                    : setPredicate({
                        value: {
                          description: predicate?.value?.description || "",
                          related: predicate?.value?.related || [],
                          broader: predicate?.value?.broader || [],
                          narrower: e.target.value.split(","),
                        },
                      });
                }}
              />
            </>
          )}
        </Form.Group>
        <Form.Group className="mb-3">
          <Form.Label>
            <i>Object</i>
          </Form.Label>
          <Form.Check
            type="switch"
            label="Concept"
            id="object-switch"
            checked={objectSwitch}
            onChange={(e) => {
              setObjectSwitch(e.target.checked);
            }}
          />
          {!objectSwitch && (
            <Form.Control
              type="text"
              onChange={(e) => setObject({ value: e.target.value })}
            />
          )}
          {objectSwitch && (
            <>
              <Form.Control
                type="text"
                placeholder="Enter concept description"
                id="object-description"
                onChange={(e) => {
                  typeof object.value === "string"
                    ? setObject({
                        value: {
                          description: e.target.value,
                          related: [],
                          broader: [],
                          narrower: [],
                        },
                      })
                    : setObject({
                        value: {
                          description: e.target.value,
                          related: object?.value?.related || [],
                          broader: object?.value?.broader || [],
                          narrower: object?.value?.narrower || [],
                        },
                      });
                }}
              />
              <Form.Control
                type="text"
                placeholder="Enter concept related entities"
                id="object-related"
                onChange={(e) => {
                  typeof object.value === "string"
                    ? setObject({
                        value: {
                          description: "",
                          related: e.target.value.split(","),
                          broader: [],
                          narrower: [],
                        },
                      })
                    : setObject({
                        value: {
                          description: object?.value?.description || "",
                          related: e.target.value.split(","),
                          broader: object?.value?.broader || [],
                          narrower: object?.value?.narrower || [],
                        },
                      });
                }}
              />
              <Form.Control
                type="text"
                placeholder="Enter concept broader entities"
                id="object-broader"
                onChange={(e) => {
                  typeof object.value === "string"
                    ? setObject({
                        value: {
                          description: "",
                          related: [],
                          broader: e.target.value.split(","),
                          narrower: [],
                        },
                      })
                    : setObject({
                        value: {
                          description: object?.value?.description || "",
                          related: object?.value?.related || [],
                          broader: e.target.value.split(","),
                          narrower: object?.value?.narrower || [],
                        },
                      });
                }}
              />
              <Form.Control
                type="text"
                placeholder="Enter concept narrower entities"
                id="object-narrower"
                onChange={(e) => {
                  typeof object.value === "string"
                    ? setObject({
                        value: {
                          description: "",
                          related: [],
                          broader: [],
                          narrower: e.target.value.split(","),
                        },
                      })
                    : setObject({
                        value: {
                          description: object?.value?.description || "",
                          related: object?.value?.related || [],
                          broader: object?.value?.broader || [],
                          narrower: e.target.value.split(","),
                        },
                      });
                }}
              />
            </>
          )}
        </Form.Group>
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
