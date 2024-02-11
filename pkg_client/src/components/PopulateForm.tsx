import Container from "react-bootstrap/esm/Container";
import Col from "react-bootstrap/esm/Col";
import Row from "react-bootstrap/esm/Row";
import Tab from "react-bootstrap/Tab";
import Nav from "react-bootstrap/Nav";
import StatementPopulationForm from "./StatementPopulationForm";
import PreferencePopulationForm from "./PreferencePopulationForm";

export interface Concept {
  description: string;
  related: string[];
  broader: string[];
  narrower: string[];
}

export interface TripleElement {
  value: string | Concept;
}

const PopulateForm = () => {
  return (
    <Container>
      <p>
        Complete the corresponding form to either add a statement or a
        preference.{" "}
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
      <Tab.Container id="left-tabs-example" defaultActiveKey="first">
        <Row>
          <Col sm={3}>
            <Nav variant="pills" className="flex-column">
              <Nav.Item>
                <Nav.Link eventKey="first">Statement</Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link eventKey="second">Preference</Nav.Link>
              </Nav.Item>
            </Nav>
          </Col>
          <Col sm={9}>
            <Tab.Content>
              {/* TODO: Add section to manage access rights of services
              See issue: https://github.com/iai-group/pkg-api/issues/66 */}
              <Tab.Pane eventKey="first">
                <StatementPopulationForm />
              </Tab.Pane>
              <Tab.Pane eventKey="second">
                <PreferencePopulationForm />
              </Tab.Pane>
            </Tab.Content>
          </Col>
        </Row>
      </Tab.Container>
    </Container>
  );
};

export default PopulateForm;
