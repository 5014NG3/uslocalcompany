import React, { useEffect, useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import Pagination from "react-bootstrap/Pagination";

export default function App() {
  const [state, setState] = useState({
    data: [],
    activePage: 1
  });

  useEffect(() => {
    // 2. Add dependency array to prevent infinite loop
    fetch(`http://localhost:5000/api/sd?offset=${10*(state.activePage-1)}`)
      .then(response => response.json())
      .then(responseData => {
        // 3. Update state properly
        setState(prevState => ({
          ...prevState,
          data: responseData
        }));
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }, [state.activePage]); // Empty dependency array

  const handlePageChange = (pageNumber) => {
    // Handle page changes here
    fetch(`http://localhost:5000/api/sd?offset=${10*(pageNumber-1)}`)
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
  };


  return (
    <div className="App">
      <h2 className="mt-5 px-4">React Bootstrap pagination example</h2>

      <ul className="list-group p-4">
        {state.data.map((item) => {
          return (
            <li key={item.id} className="list-group-item">
              <span className="font-weight-bold pr-2">{item.firm_name}.</span>{" "}
              {item.title}
            </li>
          );
        })}
      </ul>

      <Pagination className="px-4">
        {state.data.map((_, index) => {
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
