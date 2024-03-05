// Form comprising a single text input and a submit button.

import { useState } from "react";
import { Alert, Button, Spinner } from "react-bootstrap";
import Form from "react-bootstrap/Form";

interface QueryFormProps {
    handleSubmit: (query: string) => Promise<void>;
    error: string;
}

const QueryForm: React.FC<QueryFormProps> = ({ handleSubmit, error = "" }) => {
    const [query, setQuery] = useState("");
    const [isSubmitting, setIsSubmitting] = useState(false);

    const handleClick = async (query: string) => {
        try {
            setIsSubmitting(true);
            await handleSubmit(query);
            setQuery("");
        } catch (error) {
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div>
            {error && <Alert variant="danger">{error}</Alert>}
            <Form>
                <fieldset disabled={isSubmitting}>
                    <Form.Control
                        required
                        id="query-input"
                        type="text"
                        placeholder="Enter query"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                    />
                    <Button
                        id="submit-button"
                        variant="primary"
                        type="button"
                        onClick={() => handleClick(query)}
                        style={{ marginTop: "10px" }}
                        disabled={query === ""}
                    >
                        {isSubmitting ? (
                            <Spinner
                                as="span"
                                animation="border"
                                size="sm"
                                role="status"
                                aria-hidden="true"
                                style={{ marginRight: "5px" }}
                            />
                        ) : null}
                        {isSubmitting ? "Submitting..." : "Submit"}
                    </Button>
                </fieldset>
            </Form>
        </div>
    );
};

export default QueryForm;