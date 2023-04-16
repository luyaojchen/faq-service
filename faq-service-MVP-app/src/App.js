import React, { useState } from "react";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Button from "react-bootstrap/Button";

function App() {
  const [file, setFile] = useState();
  const [query, setQuery] = useState();
  const [submittedValue, setSubmittedValue] = useState();
  const [knowledgeBase, setKnowledgeBase] = useState();

  const strUrl = "http://127.0.0.1:8182";

  // uploading file to endpoint
  const AddDoc = async (file) => {
    var kb = "";
    var data = new FormData();
    await fetch(strUrl + "/create", {
      method: "GET",
      mode: "no-cors",
    })
      .then((response) => response.json())
      .then((data) => {
        setKnowledgeBase(data.knowledgebase_id);
        kb = data.knowledgebase_id;
      })
      .catch((err) => {
        console.log(err.message);
      });

    data.append("file", file);
    data.append("knowledgebase_id", kb);
    await fetch(strUrl + "/index/doc/add", {
      method: "POST",
      body: data,
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
      })
      .catch((err) => {
        console.log(err.message);
      });

    await fetch(strUrl + "/compose?knowledgebase_id=" + kb, {
      method: "GET",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
      })
      .catch((err) => {
        console.log(err.message);
      });
  };

  // handler for selecting file
  function handleChange(event) {
    setFile(event.target.files[0]);
  }

  // handler for submitting button
  const submitFile = async () => {
    await AddDoc(file);
    setSubmittedValue(file);
  };

  // handler for submitting question
  const uppdateQuery = () => {
    var message = document.getElementById("query").value;
    setQuery(message);
  };

  // handler for submitting question
  const submitQuestion = () => {
    var message = document.getElementById("query").value;
    setQuery(message);
    console.log(query);
  };

  return (
    <Container fluid>
      <Row
        style={{
          backgroundColor: "aqua",
          height: "5rem",
        }}
      >
        header for faq service
      </Row>
      <Row>
        {!submittedValue ? (
          <Row id="dropBox" className="SubmitContainer">
            <p>Click to select</p>
            <input type="file" id="fileInput" onChange={handleChange} />
            <Button as="input" type="submit" onClick={submitFile} />
          </Row>
        ) : (
          <Row>
            <textarea
              placeholder="Ask your question!"
              id="query"
              onChange={uppdateQuery}
            ></textarea>
            <br />
            <Button as="input" type="submit" onClick={submitQuestion} />
            <br />
            <textarea readOnly placeholder="Answer"></textarea>
          </Row>
        )}
      </Row>
    </Container>
  );
}

export default App;
