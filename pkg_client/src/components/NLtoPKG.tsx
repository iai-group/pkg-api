// Natural language to PKG component

import { Button, Container } from "react-bootstrap";
import { UserContext } from "../contexts/UserContext";
import { useContext, useState } from "react";
import axios from "axios";
import QueryForm from "./QueryForm";

const NLtoPKG = () => {
  const { user } = useContext(UserContext);
  const [error, setError] = useState("");
  const [info, setInfo] = useState("");
  const [pkgHide, setPkgHide] = useState(true);

  const baseURL =
    (window as any)["PKG_API_BASE_URL"] || "http://127.0.0.1:5000";

  const getImage = async () => {
    let imageURL = null;
    await axios
      .get(`${baseURL}/explore`, {
        params: {
          owner_username: user?.username,
          owner_uri: user?.uri,
        },
        responseType: "blob",
      })
      .then((response) => {
        setError("");
        imageURL = URL.createObjectURL(
          new Blob([response.data], {
            type: "image/png",
          })
        );
      })
      .catch((error) => {
        setError(error.message);
        console.log(error);
        throw error;
      });
    return imageURL;
  };

  const updateImage = async () => {
    const informationDiv = document.getElementById("information-container");
    const previousImage = informationDiv?.getElementsByTagName("img")[0];
    setPkgHide(!pkgHide);
    if (!pkgHide === true) {
      if (previousImage) {
        previousImage.remove();
      }
    } else {
      let imagePath = await getImage();
      if (imagePath) {
        if (previousImage) {
          previousImage.src = imagePath;
        } else {
          const image = document.createElement("img");
          image.src = imagePath;
          image.alt = "PKG";
          image.style.width = "100%";
          informationDiv?.appendChild(image);
        }
      }
    }
  };

  const handleSubmit = (query: string) => {
    return axios
      .post(`${baseURL}/nl`, {
        query: query,
        owner_username: user?.username,
        owner_uri: user?.uri,
      })
      .then((response) => {
        setInfo(response.data.message);
        setError("");
        console.log(response);
        if (pkgHide === false) {
          updateImage();
        }
      })
      .catch((error) => {
        setInfo("");
        setError(error.message);
        throw error;
      });
  };

  return (
    <Container>
      <div>
        <b>Manage your PKG with natural language queries.</b>
      </div>
      <QueryForm handleSubmit={handleSubmit} error={error} />
      <br />
      <div id="information-container">
        {info && <div>Query execution status: {info}</div>}
        <Button onClick={updateImage} variant="secondary" size="sm">
          {pkgHide ? "Show" : "Hide"} PKG
        </Button>
      </div>
    </Container>
  );
};

export default NLtoPKG;
