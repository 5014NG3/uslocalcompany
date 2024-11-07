import React, { useEffect, useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { Pagination, Dropdown, Container, Col, Row } from "react-bootstrap";
import state_meta_data from "./data/sba_city_meta.json"




export default function App() {
  const [state, setState] = useState({
    data: [],
    activePage: 1,
    stateName: "",
    city: "",
    biz_count: 0

  });

  useEffect(() => {
    if (state.city !== "" && state.stateName !== "" && !isNaN(state.activePage) && state.activePage > 0) {
      fetch(`http://localhost:5000/api/${state.stateName}?city=${state.city}&offset=${10 * (state.activePage - 1)}`)
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
  }, [state.activePage, state.stateName, state.city]);

  const handlePageChange = (pageNumber) => {

    if (state.city !== "" && state.stateName !== "" && !isNaN(state.activePage) && state.activePage > 0) {
      fetch(`http://localhost:5000/api/${state.stateName}?city=${state.city}&offset=${10 * (pageNumber - 1)}`)
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
      stateName: new_state,
      city: "",
      biz_count: 0,
      data: [],
      activePage: 1

    }));
  }

  const handleCityChange = (new_city, business_count) => {
    setState(prevState => ({
      ...prevState,
      city: new_city,
      biz_count: business_count,
      activePage: 1,
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
                  <Dropdown.Item key={item.city} onClick={() => handleCityChange(item.city, item.business_count)}>{item.city}</Dropdown.Item>
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
        {[...Array(Math.ceil(state.biz_count/10))].map((_, index) => {
          const pageNumber = index + 1;
          return (
            <Pagination.Item
              onClick={() => handlePageChange(pageNumber)}
              key={pageNumber}
              active={pageNumber === state.activePage}
            >
              {pageNumber}
            </Pagination.Item>
          );
        })}
      </Pagination>



    </div>
  );
}
