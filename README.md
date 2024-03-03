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

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- This project was inspired by the need to automate the collection of lotto results for analysis and historical record-keeping.
- Special thanks to the developers of aiohttp, pandas, and SQLAlchemy for their excellent libraries.


## Analysis Results

<!--START_SECTION:analysis-->
{{analysis_placeholder}}
<h1>Lottery Analysis Report</h1>
            <div class="basic-analysis">
                <h2>Basic Analysis:</h2>
                <p>Total number of draws: 2306<br></p>
            </div>
            <div class="additional-analysis">
                <h2>Additional Data:</h2>
                <p><br>Latest Entry Analysis:<br>- Draw Date: 2024-03-02<br>- Draw Number: 2306<br>- Numbers Drawn: 4-5-10-24-27<br>- Power Ball: 7<br>- Multiplier: 4<br>- Jackpot: 0<br>- Wins: -1<br></p>
            </div>
            <div class="average-jackpot">
                <h2>Average Jackpot Amount:</h2>
                <p>$3,610,127.19</p>
            </div>
            <div class="numbers-drawn">
                <h2>Numbers Drawn:</h2>
                <p>4, 5, 10, 24, 27</p>
            </div>
            <div class="most-common-numbers">
                <h2>Most Common Numbers Drawn:</h2>
                <table>
                    <tr>
                        <th>Number</th>
                        <th>Frequency</th>
                    </tr>
                    <tr><td>29</td><td>353 times
</td></tr><tr><td>25</td><td>353 times
</td></tr><tr><td>34</td><td>351 times
</td></tr><tr><td>27</td><td>346 times
</td></tr><tr><td>13</td><td>345 times
</td></tr>
                </table>
            </div>
        