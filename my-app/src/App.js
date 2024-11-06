import React, { useEffect, useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { Pagination, Dropdown, Container, Col, Row } from "react-bootstrap";
import state_meta_data from "./data/sba_city_meta.json"


export default function App() {
  const [state, setState] = useState({
    data: [],
    activePage: 1,
    stateName: "sd",
    city: "",
    biz_count: 0

  });

  useEffect(() => {
    if (state.stateName !== "" && !isNaN(state.activePage) && state.activePage > 0) {
      fetch(`http://localhost:5000/api/${state.stateName}?offset=${10 * (state.activePage - 1)}`)
        .then(response => response.json())
        .then(responseData => {
          setState(prevState => ({
            ...prevState,
            data: responseData
          }));
        })
        .catch(error => {
          console.error('Error fetching data:', error);
        });
    }
  }, [state.activePage, state.stateName]);

  const handlePageChange = (pageNumber) => {

    if (state.stateName !== "" && !isNaN(state.activePage) && state.activePage > 0) {
      fetch(`http://localhost:5000/api/${state.stateName}?offset=${10 * (pageNumber - 1)}`)
        .then(response => response.json())
        .then(responseData => {
          setState(prevState => ({
            ...prevState,
            data: responseData,
            activePage: pageNumber
          }));
        })
        .catch(error => {
          console.error('Error fetching data:', error);
        });
    }
  };

  const handleStateChange = (new_state) => {
    setState(prevState => ({
      ...prevState,
      stateName: new_state
    }));
  }

  const handleCityChange = (new_city) => {
    setState(prevState => ({
      ...prevState,
      city: new_city
    }));
  }


  return (
    <div className="App">
      <h2 className="mt-5 px-4">US Small bizzes</h2>

      <Container>

        <Row>

          <Col xs="auto">
            <Dropdown>
              <Dropdown.Toggle variant="success" id="dropdown-basic">
                State
              </Dropdown.Toggle>

              <Dropdown.Menu style={{ minWidth: '1vh', maxHeight: '25vh', overflowY: 'auto' }}>
                {Object.keys(state_meta_data).map((key) => (
                  <Dropdown.Item key={key} onClick={() => handleStateChange(key)}>{key}</Dropdown.Item>
                ))}
              </Dropdown.Menu>
            </Dropdown>
          </Col>


          <Col xs="auto">
            <Dropdown>
              <Dropdown.Toggle variant="success" id="dropdown-basic">
                City
              </Dropdown.Toggle>

              <Dropdown.Menu style={{ maxHeight: '25vh', overflowY: 'auto' }}>
                {state_meta_data[state.stateName]?.map((item) => (
                  <Dropdown.Item key={item.city} onClick={() => handleCityChange(item.city)}>{item.city}</Dropdown.Item>
                ))}
              </Dropdown.Menu>
            </Dropdown>
          </Col>
        </Row>


      </Container>



      <ul className="list-group p-4">
        {state.data.map((item) => {
          return (
            <li key={item.index} className="list-group-item">
              <span className="font-weight-bold pr-2">{item.firm_name}.</span>{" "}
              {item.area}
            </li>
          );
        })}
      </ul>

      <Pagination className="px-4">
        {Array(6).fill(null, 0, 5).map((_, index) => {
          return (
            <Pagination.Item
              onClick={() => handlePageChange(index + 1)}
              key={index + 1}
              active={index + 1 === state.activePage}
            >
              {index + 1}
            </Pagination.Item>
          );
        })}
      </Pagination>



    </div>
  );
}
