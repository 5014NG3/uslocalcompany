# Local Business Finder (United States)

A web application for searching small businesses in the United States by state and city/zip code.

## Features:

### Web Scraper:
- Scrapes small business data (city/zip code level) from Small Business Administration(SBA)'s [DSBS](https://dsbs.sba.gov/search/dsp_dsbs.cfm) using Python.
- Utilizes **BeautifulSoup** to parse HTML data from each page.
- **Pandas** is used for cleaning and processing the scraped data.
- Data is stored in an **SQLite** database.

### Backend:
- **Flask** server with a basic **API** to query the SQLite database by state and city.

### Frontend:
- **React** app for the user interface.
- Uses **React-Bootstrap** for responsive design.
- **React-Select** is used for state and city selection.

### Instruction:
- Idk figure what packages you need to install
- cd into my-app
- npm start

