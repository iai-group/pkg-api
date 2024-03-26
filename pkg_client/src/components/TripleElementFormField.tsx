import { useState } from "react";
import ConceptFormField, { Concept } from "./ConceptFormField";
import Form from "react-bootstrap/Form";

export interface TripleElement {
  value: string | Concept;
}

export interface TripleElementFormFieldProps {
  label: string;
  value: TripleElement;
  onChange: (value: TripleElement) => void;
}

const TripleElementFormField: React.FC<TripleElementFormFieldProps> = ({
  label,
  value,
  onChange,
}) => {
  const [conceptSwitch, setConceptSwitch] = useState(false);
  const [tripleElement, setTripleElement] = useState<TripleElement>({
    value: value.value ?? "",
  });

  const handleConceptChange = (updatedConcept: Concept) => {
    setTripleElement({ value: updatedConcept });
    onChange({ value: updatedConcept });
  };

  return (
    <>
      <Form.Group className="mb-3">
        <Form.Label>{label}</Form.Label>
        <Form.Check
          type="switch"
          id={`${label}-switch`}
          label="Concept"
          checked={conceptSwitch}
          onChange={(e) => {
            setConceptSwitch(e.target.checked);
          }}
        />
        {!conceptSwitch ? (
          <Form.Control
            type="text"
            value={tripleElement.value as string}
            onChange={(e) => {
              setTripleElement({ value: e.target.value });
            }}
          />
        ) : (
          <ConceptFormField
            value={tripleElement.value as Concept}
            onChange={handleConceptChange}
          />
        )}
      </Form.Group>
    </>
  );
};

export default TripleElementFormField;
