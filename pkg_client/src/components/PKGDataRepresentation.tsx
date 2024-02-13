import { useContext, useEffect, useState } from "react";
import { UserContext } from "../contexts/UserContext";

interface PKGDatRepresentationProps {
  data: any;
}

const PKGDatRepresentation: React.FC<PKGDatRepresentationProps> = ({
  data,
}) => {
  const { user } = useContext(UserContext);
  const [interpretation, setInterpretation] = useState("");

  const generateInterpretation = (data: any) => {
    const isUrl = (value: string) => {
      try {
        return Boolean(new URL(value));
      } catch (e) {
        return false;
      }
    };

    let subject = data.triple.subject;
    let interpretation = "";
    if (subject?.reference) {
      subject = subject.reference;
    } else {
      if (typeof subject.value !== "string") {
        subject = subject.value.description;
      } else {
        subject = subject.value;
      }
    }

    if (subject === "I" || subject === "i" || subject === user?.uri) {
      subject = "you";
    }

    if (data.preference) {
      let object = data.preference.topic.value;
      if (typeof object !== "string") {
        object = data.preference.topic.value.description;
      } else {
        if (isUrl(object)) {
          object =
            "<a href='" +
            object +
            "'>" +
            object.split("/").pop()?.replaceAll("_", " ") +
            "</a>";
        }
      }
      if (data.preference.weight === -1) {
        interpretation =
          subject + ' expressed a negative preference towards "' + object + '"';
      } else if (data.preference.weight === 1) {
        interpretation =
          subject + ' expressed a positive preference towards "' + object + '"';
      }
    } else {
      interpretation = "This statement is a fact about " + subject;
    }

    setInterpretation("<p> Interpretation: " + interpretation + ".</p>");
  };

  useEffect(() => {
    generateInterpretation(data);
  }, [data]);

  return (
    <div>
      {interpretation ? (
        <>
          <b>Below you can see how your statement was interpreted.</b>
          <p>Statement: {data.statement}</p>
          <span dangerouslySetInnerHTML={{ __html: interpretation }}></span>
        </>
      ) : null}
    </div>
  );
};

export default PKGDatRepresentation;
