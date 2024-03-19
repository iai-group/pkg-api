// Layout component for the application includes a navigation bar and content
// of the current tab.
import { Outlet, Link } from "react-router-dom";
import Nav from "react-bootstrap/Nav";
import { useState } from "react";

const Layout = () => {
  const [activeKey, setActiveKey] = useState("/");

  const handleSelect = (eventKey: string | null) => {
    if (eventKey !== null) {
      setActiveKey(eventKey);
    }
  };

  return (
    <>
      <Nav variant="underline" activeKey={activeKey} onSelect={handleSelect}>
        <Nav.Item>
          <Nav.Link eventKey="/" as={Link} to="/">
            Home
          </Nav.Link>
        </Nav.Item>
        <Nav.Item>
          <Nav.Link eventKey="/service" as={Link} to="/service">
            Service Management
          </Nav.Link>
        </Nav.Item>
        <Nav.Item>
          <Nav.Link eventKey="/population" as={Link} to="/population">
            Populate PKG
          </Nav.Link>
        </Nav.Item>
        <Nav.Item>
          <Nav.Link eventKey="/explore" as={Link} to="/explore">
            Explore PKG
          </Nav.Link>
        </Nav.Item>
      </Nav>

      <br />
      <Outlet />
    </>
  );
};

export default Layout;
