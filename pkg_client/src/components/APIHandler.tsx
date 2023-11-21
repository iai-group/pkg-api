import React, { useEffect, useState } from "react";
import axios from "axios";

const APIHandler: React.FC = () => {
  // State tracker for authentication data, i.e. is user logged in?
  const [authData, setAuthData] = useState(null);
  // State tracker for service management data.
  const [serviceData, setServiceData] = useState(null);
  // State tracker for personal facts data.
  const [factsData, setFactsData] = useState(null);
  // State tracker for PKG exploration data. Data presentation, graphs, etc.
  const [exploreData, setExploreData] = useState(null);

  useEffect(() => {
    const baseURL =
      (window as any)["PKG_API_BASE_URL"] || "http://localhost:5000";

    axios.get(`${baseURL}/auth`).then((response) => setAuthData(response.data));
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
    <div>
      <h1>Personal Knowledge Graph API</h1>
      <div>
        <h2>Auth Data</h2>
        <pre>{JSON.stringify(authData, null, 2)}</pre>
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
    </div>
  );
};

export default APIHandler;
