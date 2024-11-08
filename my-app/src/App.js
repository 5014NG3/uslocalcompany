import React, { useEffect, useState} from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { Pagination, Container, Col, Row, Card, Button , Stack, Badge} from "react-bootstrap";
import state_meta_data from "./data/sba_city_meta.json"
import Select from 'react-select'

const area_to_name = {
  "RAD" : "Research & Development",
  "SVC" : "Service",
  "MFG" : "Manufacturing",
  "CON" : "Construction"
}

const area_to_color = {
  "RAD" : "success",
  "SVC" : "danger",
  "MFG" : "primary",
  "CON" : "secondary"
}


const abbreviation_to_name = {
  "AK": "Alaska",
  "AL": "Alabama",
  "AR": "Arkansas",
  "AZ": "Arizona",
  "CA": "California",
  "CO": "Colorado",
  "CT": "Connecticut",
  "DE": "Delaware",
  "FL": "Florida",
  "GA": "Georgia",
  "HI": "Hawaii",
  "IA": "Iowa",
  "ID": "Idaho",
  "IL": "Illinois",
  "IN": "Indiana",
  "KS": "Kansas",
  "KY": "Kentucky",
  "LA": "Louisiana",
  "MA": "Massachusetts",
  "MD": "Maryland",
  "ME": "Maine",
  "MI": "Michigan",
  "MN": "Minnesota",
  "MO": "Missouri",
  "MS": "Mississippi",
  "MT": "Montana",
  "NC": "North Carolina",
  "ND": "North Dakota",
  "NE": "Nebraska",
  "NH": "New Hampshire",
  "NJ": "New Jersey",
  "NM": "New Mexico",
  "NV": "Nevada",
  "NY": "New York",
  "OH": "Ohio",
  "OK": "Oklahoma",
  "OR": "Oregon",
  "PA": "Pennsylvania",
  "RI": "Rhode Island",
  "SC": "South Carolina",
  "SD": "South Dakota",
  "TN": "Tennessee",
  "TX": "Texas",
  "UT": "Utah",
  "VA": "Virginia",
  "VT": "Vermont",
  "WA": "Washington",
  "WI": "Wisconsin",
  "WV": "West Virginia",
  "WY": "Wyoming",
  "DC": "District of Columbia",
  "AS": "American Samoa",
  "GU": "Guam GU",
  "MP": "Northern Mariana Islands",
  "PR": "Puerto Rico PR",
  "VI": "U.S. Virgin Islands",
}



const query_offset = 20

function GetAreaBadges({ areas }) {
  const words = areas.split(" "); 
  return (
    <Stack direction="horizontal" gap={2} className = "pb-3" >
      {words.map((area, index) => (
        <Badge style={{fontSize: '1.05rem'}} bg = {area_to_color[area]} key={index}>{area_to_name[area]}</Badge>
      ))}
    </Stack>
  );
}


function CreateLink({link}){
  const protocol = "http";

  if (link.toLowerCase().startsWith(protocol)){
    return <a href={link} target="_blank" rel="noopener noreferrer">{link}</a>
  }

  else{
    return <span>{link}</span>
  }
}



function HorizontalCard({item}) {

  //"view","firm_name","person","title","address_line_1","address_line_2","city","state","zip","capabilities",
  //"email","website","area","plusfour","full_zip","actual_city"
  return (
    <Card  style = {{maxWidth : "150vh"}}>
      <Card.Header as="h4">{item.firm_name}</Card.Header>
      <Card.Body>
        <Card.Title as="h5">{item.person}{item.title ? `, ${item.title}` : ''}</Card.Title>
        <Card.Text>{`${item.address_line_1} ${item.address_line_2}, ${item.actual_city}, ${item.state}, ${item.full_zip}`}</Card.Text>
        <Card.Text> <CreateLink link={item.website} /> </Card.Text>
        <Card.Text>{item.email}</Card.Text>
        <Card.Text> {item.capabilities} </Card.Text>
        <GetAreaBadges areas={item.area} />


        <Button variant="primary">Go somewhere</Button>

      </Card.Body>
    </Card>
  );
}


export default function App() {
  const [state, setState] = useState({
    data: [],
    activePage: 1,
    stateName: "",
    city: "",
    biz_count: 0

  });

  useEffect(() => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  }, [state.data]);





  useEffect(() => {
    if (state.city !== "" && state.stateName !== "" && !isNaN(state.activePage) && state.activePage > 0) {
      fetch(`http://localhost:5000/api/${state.stateName}?city=${state.city}&offset=${query_offset * (state.activePage - 1)}`)
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
      fetch(`http://localhost:5000/api/${state.stateName}?city=${state.city}&offset=${query_offset * (pageNumber - 1)}`)
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
      <Container className="d-flex">
        <Row >
          <Col  >
            <Select
              
              placeholder="State"
              onChange={(option) => handleStateChange(option.value)}
              styles={{
                control: (base) => ({
                  ...base,
                  width: '25vh',
                  backgroundColor: 'var(--bs-body-bg)',

                }),
                menu: (base) => ({
                  ...base,
                  width: '25vh',
                  backgroundColor: 'var(--bs-body-bg)',
                  color: 'var(--bs-body-color)',
                  zIndex: 9999, // Set a very high zIndex

                }),
                singleValue: (base) => ({
                  ...base,
                  color: 'var(--bs-body-color)'
                }),
                placeholder: (base) => ({
                  ...base,
                  color: 'var(--bs-body-color)'
                }),
                input: (base) => ({
                  ...base,
                  color: 'var(--bs-body-color)'
                }),
                option: (base, state) => ({
                  ...base,
                  backgroundColor: state.isSelected
                    ? 'var(--bs-primary)'         // Color for selected option
                    : state.isFocused
                      ? 'var(--bs-primary)'     // Color when hovering
                      : 'var(--bs-body-bg)'
                })

              }}
              options={Object.keys(state_meta_data).map(key => ({ value: key, label: abbreviation_to_name[key] }))}

            />
          </Col>

          <Col >
            <Select placeholder="City"
              key={state.stateName}
              onChange={(option) => handleCityChange(option.value.city, option.value.business_count)}
              styles={{
                control: (base) => ({
                  ...base,
                  backgroundColor: 'var(--bs-body-bg)',
                  width: '25vh',

                }),
                menu: (base) => ({
                  ...base,
                  width: '25vh',
                  backgroundColor: 'var(--bs-body-bg)',
                  zIndex: 9999, // Set a very high zIndex

                }),
                singleValue: (base) => ({
                  ...base,
                  color: 'var(--bs-body-color)'
                }),
                placeholder: (base) => ({
                  ...base,
                  color: 'var(--bs-body-color)'
                }),
                input: (base) => ({
                  ...base,
                  color: 'var(--bs-body-color)'
                }),
                option: (base, state) => ({
                  ...base,
                  backgroundColor: state.isSelected
                    ? 'var(--bs-primary)'         // Color for selected option
                    : state.isFocused
                      ? 'var(--bs-primary)'     // Color when hovering
                      : 'var(--bs-body-bg)'
                })

              }}
              options={state_meta_data[state.stateName]?.map((item) => ({ value: item, label: item.city }))} />
          </Col>
        </Row>

      </Container>



      <ul className="list-group p-4">
        {state.data.map((item, index) => {
          return (  

            <div key = {index} className = "pb-5" >
              <HorizontalCard item = {item}/>
            </div>


          );
        })}
      </ul>



      <Pagination className="px-4">
        {[...Array(Math.ceil(state.biz_count / 20))].map((_, index) => {
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
