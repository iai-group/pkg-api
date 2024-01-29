import React, { useContext, useEffect, useState } from "react";
import axios from "axios";
import { UserContext } from "../contexts/UserContext";
import Container from "react-bootstrap/Container";

const APIHandler: React.FC = () => {
  const { user } = useContext(UserContext);
  // State tracker for service management data.
  const [serviceData, setServiceData] = useState(null);
  // State tracker for personal facts data.
  const [factsData, setFactsData] = useState(null);
  // State tracker for PKG exploration data. Data presentation, graphs, etc.
  const [exploreData, setExploreData] = useState(null);

  useEffect(() => {
    const baseURL =
      (window as any)["PKG_API_BASE_URL"] || "http://localhost:5000";

    axios
      .get(`${baseURL}/service`)
      .then((response) => setServiceData(response.data));
    axios
      .get(`${baseURL}/facts`)
      .then((response) => setFactsData(response.data));
    axios
      .get(`${baseURL}/explore`)
      .then((response) => setExploreData(response.data));
  }, []);

  return (
    <Container>
      <h1>Personal Knowledge Graph API</h1>
      <div>
        <p>Welcome {JSON.stringify(user, null, 2)}</p>
      </div>
      <div>
        <h2>Service Management Data</h2>
        <pre>{JSON.stringify(serviceData, null, 2)}</pre>
      </div>
      <div>
        <h2>Personal Facts Data</h2>
        <pre>{JSON.stringify(factsData, null, 2)}</pre>
      </div>
      <div>
        <h2>PKG Exploration Data</h2>
        <pre>{JSON.stringify(exploreData, null, 2)}</pre>
      </div>
    </Container>
  );
};

export default APIHandler;
