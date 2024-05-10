import Container from "react-bootstrap/esm/Container";
import StatementPopulationForm from "./StatementPopulationForm";

const PopulateForm = () => {
  return (
    <Container>
      <p>
        Complete the corresponding form to either add or delete a statement.{" "}
        <b>
          It is assumed that you are familiar with the{" "}
          <a href="https://iai-group.github.io/pkg-vocabulary/" target="blank">
            PKG vocabulary
          </a>
          .
        </b>
      </p>
      <p>
        By default the annotations are URIs but if they are not available, you
        can use concepts instead.
      </p>

      {/* TODO: Add section to manage access rights of services
              See issue: https://github.com/iai-group/pkg-api/issues/66 */}
      <StatementPopulationForm />
    </Container>
  );
};

export default PopulateForm;
