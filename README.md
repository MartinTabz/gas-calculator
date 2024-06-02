
# Gas Calculator

Small Python project for dynamic calculation of total gas price between two locations.


## Features

- Configuration
    - Google Cloud Console API Key
    - Car fuel consumption
    - Car fuel type
- Querying path information from Google Distance API
- Scraping current price of selected fuel type [(Tank ONO)](https://tank-ono.cz/cz/index.php?page=cenik)
- Saving queries to CSV file


## Run Locally

Clone the project

```bash
  git clone https://github.com/MartinTabz/gas-calculator.git
```

Go to the project directory

```bash
  cd gas-calculator
```

Install libraries

```bash
  pip install bs4 googlemaps requests
```

Start the scipt

```bash
  python script.py
```

