import { useContext, useEffect, useState } from "react";
import { UserContext } from "../contexts/UserContext";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import { TripleElement } from "./PopulateForm";
import { Alert } from "react-bootstrap";
import axios from "axios";

const PreferencePopulationForm = () => {
  const { user } = useContext(UserContext);
  const [error, setError] = useState("");
  const [info, setInfo] = useState("");
  const [subject, setSubject] = useState("");
  const [objectSwitch, setObjectSwitch] = useState(false);
  const [object, setObject] = useState<TripleElement>({
    value: "",
  });
  const [prefValue, setPrefValue] = useState(Number.NaN);
  const [statementID, setStatementID] = useState("");
  const baseURL =
    (window as any)["PKG_API_BASE_URL"] || "http://127.0.0.1:5000";

  useEffect(() => {
    setObject((newValue) => ({
      value:
        typeof newValue.value === "string"
          ? newValue.value
          : {
              description: newValue.value.description,
              related: newValue.value.related || [],
              broader: newValue.value.broader || [],
              narrower: newValue.value.narrower || [],
            },
    }));
  }, [object]);

  const addPreference = () => {
    if (!subject) {
      setError("Please fill the required field: Subject.");
      return;
    }
    if (isNaN(prefValue)) {
      setError("Please fill the required field: Preference value.");
      return;
    }
    if (typeof object.value === "string" && object.value === "") {
      setError("Please fill the required field: Object.");
      return;
    } else if (
      typeof object.value !== "string" &&
      object.value.description === ""
    ) {
      setError("Please fill the required field: Object description.");
      return;
    }
    // Axios sent POST request with body
    axios
      .post(`${baseURL}/preference`, {
        subject: subject,
        object: object.value,
        preference: prefValue,
        statementID: statementID,
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
            placeholder="Enter subject URI"
            onChange={(e) => setSubject(e.target.value)}
          />
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
        <Form.Group className="mb-3">
          <Form.Label>
            <i>Origin statement ID</i>
          </Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter statement ID"
            onChange={(e) => setStatementID(e.target.value)}
          />
        </Form.Group>
        <Button
          className="mt-3"
          style={{ marginRight: "10px" }}
          variant="primary"
          onClick={addPreference}
        >
          Add preference
        </Button>
      </Form>
    </>
  );
};

export default PreferencePopulationForm;