import { useState } from "react";
import Form from "react-bootstrap/Form";

export interface Concept {
  description: string;
  related_entities: string[];
  broader_entities: string[];
  narrower_entities: string[];
}

export interface ConceptFormFieldProps {
  value?: Concept;
  onChange: (value: Concept) => void;
}

const ConceptFormField: React.FC<ConceptFormFieldProps> = ({
  value,
  onChange,
}) => {
  const [fieldValue, setFieldValue] = useState<Concept>(
    value || {
      description: "",
      related_entities: [],
      broader_entities: [],
      narrower_entities: [],
    }
  );

  const onElementChange = (newValue: Partial<Concept>) => {
    setFieldValue({ ...fieldValue, ...newValue });
    onChange({ ...fieldValue, ...newValue });
  };

  return (
    <>
      <Form.Control
        type="text"
        placeholder="Enter concept description"
        value={fieldValue.description}
        onChange={(e) => onElementChange({ description: e.target.value })}
      />
      <Form.Control
        type="text"
        placeholder="Enter related entities"
        value={fieldValue.related_entities?.join(",")}
        onChange={(e) =>
          onElementChange({
            related_entities: e.target.value.split(",").map((e) => e.trim()),
          })
        }
      />
      <Form.Control
        type="text"
        placeholder="Enter broader entities"
        value={fieldValue.broader_entities?.join(",")}
        onChange={(e) =>
          onElementChange({
            broader_entities: e.target.value.split(",").map((e) => e.trim()),
          })
        }
      />
      <Form.Control
        type="text"
        placeholder="Enter narrower entities"
        value={fieldValue.narrower_entities?.join(",")}
        onChange={(e) =>
          onElementChange({
            narrower_entities: e.target.value.split(",").map((e) => e.trim()),
          })
        }
      />
    </>
  );
};

export default ConceptFormField;
