import React, { useState } from "react";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Button from "react-bootstrap/Button";

function App() {
  const [file, setFile] = useState();
  const [query, setQuery] = useState();
  const [submittedValue, setSubmittedValue] = useState();
  const [knowledgebase, setKnowledgebase] = useState();

  const strUrl = "http://127.0.0.1:8182";

  const AddDoc = async (file) => {
    var kb = "";
    var data = new FormData();
    await fetch(strUrl + "/create", {
      method: "GET",
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        console.log(data);
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
    return kb;
  };

  const AskQuestion = async () => {
    var text = "";
    await fetch(
      strUrl + "/query?knowledgebase_id=" + knowledgebase + "&query=" + query,
      {
        method: "GET",
      }
    )
      .then((response) => {
        return response.text();
      })
      .then((data) => {
        console.log(data);
        text = data;
      })
      .catch((err) => {
        console.log(err.message);
      });
    return text;
  };

  // handler for selecting file
  function handleChange(event) {
    setFile(event.target.files[0]);
  }

  // handler for submitting button
  const submitFile = async () => {
    const kb = await AddDoc(file);
    setKnowledgebase(kb);
    setSubmittedValue(file);
  };

  // handler for submitting question
  const uppdateQuery = () => {
    var message = document.getElementById("query").value;
    setQuery(message);
  };

  // handler for submitting question
  const submitQuestion = async () => {
    var message = document.getElementById("query").value;
    setQuery(message);
    const text = await AskQuestion();
    document.getElementById("ans").value = text;
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
            <textarea id="ans" readOnly placeholder="Answer"></textarea>
          </Row>
        )}
      </Row>
    </Container>
  );
}

export default App;
