# Lotto Results Web Scraper

This is a Python web scraper designed to fetch lotto results from a specified website and store them in a SQLite database. It utilizes asyncio and aiohttp for asynchronous web scraping and SQLAlchemy for database operations.

## Features

- Asynchronous fetching of lotto results from a specified website.
- Parsing of fetched data and storage in a SQLite database.
- Automated stopping at the current month and year to avoid fetching future lotto results.
- Error handling and logging for robustness and reliability.

## Requirements

- Python 3.7 or higher
- aiohttp
- pandas
- SQLAlchemy

## Installation

1. Clone the repository.
2. Install the required dependencies.

## Usage

1. Modify the `urls` variable in `async_scraper.py` to include the URLs of the websites containing lotto results.
2. Run the scraper.
3. The scraper will fetch lotto results, parse them, and store them in the SQLite database.

## Configuration

- You can customize the database name and location by modifying the `Database_Name` and `Location` variables in `async_scraper.py`.
- Adjust the scraping frequency by modifying the `YEAR` and `MONTH` variables in `async_scraper.py` to include the desired range of years and months.

## Contributing

Contributions are welcome! If you find any bugs or have suggestions for improvement, please open an issue or submit a pull request.

## GitHub Actions

This repository includes a GitHub Actions workflow that automatically performs analysis on the scraped lotto results. The workflow is triggered on each push to the `main` branch. It runs a Python script to analyze the data and generates reports.

### Analysis Results

<!--START_SECTION:analysis-->
    
    
<!--END_SECTION:analysis-->


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- This project was inspired by the need to automate the collection of lotto results for analysis and historical record-keeping.
- Special thanks to the developers of aiohttp, pandas, and SQLAlchemy for their excellent libraries.

