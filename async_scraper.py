import asyncio
import aiohttp
import pandas as pd
from io import StringIO
import os
import datetime
from uuid import uuid4
import warnings
from time import perf_counter
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, Date, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

warnings.simplefilter(action='ignore', category=FutureWarning)

MONTH = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
YEAR = ['{:02d}'.format(i) for i in range(0, 25)]

cwd = os.getcwd()
Database_Name = 'Lotto_Results_Database.db'
Location = r'Database'
WorkingDir = os.path.join(cwd, Location)
if not os.path.exists(WorkingDir):
    os.mkdir(WorkingDir)

Database = os.path.join(WorkingDir,  Database_Name)

Base = declarative_base()

class Lotto_Result(Base):
    __tablename__ = 'lotto_data'

    DrawDate = Column(Date, primary_key=True)
    DrawNum = Column(String)
    Numbers = Column(String)
    Power_Ball = Column(String)
    Multiplier = Column(String)
    Jackpot = Column(String)
    Wins = Column(String)
    uniqueId = Column(String)
    last_updated = Column(Date)
    date_created = Column(Date)

    def __init__(self, DrawDate, DrawNum, Numbers, Power_Ball, Multiplier, Jackpot, Wins):
        self.DrawDate = DrawDate
        self.DrawNum = DrawNum
        self.Numbers = Numbers
        self.Power_Ball = Power_Ball
        self.Multiplier = Multiplier
        self.Jackpot = Jackpot
        self.Wins = Wins
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
        if self.date_created is None:
            self.date_created = datetime.datetime.now()
        self.last_updated = datetime.datetime.now()

    def __repr__(self):
        return f"<Lotto_Result(DrawDate ='{self.DrawDate}'>"

def clean_jp(row):
    try:
        return float(str(row).replace('$','').replace(',',''))
    except : return 0

class WebScraper:
    def __init__(self, urls):
        self.urls = urls
        self.ParsedData = []

    async def fetch(self, session, year, month, url):
        params = {'monthyear': f'{month}-{year}', 'sid':'cb4a924b4b574e20dab97df23823194e92a644245b46a62e6a0111674afbbf4b'}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0'}
           
       
        retries = 3
        for attempt in range(retries):
            try:
                async with session.get(url, params=params, headers=headers) as response:
                    if response.status == 200:
                        try:
                            content = await response.text()
                            html_data = StringIO(content)
                            df = pd.read_html(html_data)[0].dropna(how='all')
                            dates = df.iloc[::2].reset_index().drop(columns=['index']).rename(columns={'Draw#': 'Date'})['Date']
                            data = df.iloc[1::2].reset_index().drop(columns=['index'])
                            table = pd.merge(dates, data, left_index=True, right_index=True).copy()
                            table['Date'] = pd.to_datetime(table['Date'], dayfirst=True,format="%d-%b-%y").dt.strftime('%Y-%m-%d')
                            print('[*] Data Scraped : ', params['monthyear'])

                            table['Jackpot']    = table['Jackpot'].apply(clean_jp)
                            table['Draw#']      = table['Draw#'].astype(int)
                            table['Power Ball'] = table['Power Ball'].astype(int)
                            table['Multiplier'] = table['Multiplier'].fillna(-1).astype(int)
                            table['Wins']       = table.Wins.str.replace("X",'-1').astype(int)
                            return table.to_dict('records')
                        except Exception as e:
                            print(f'[*] Error {e} Occurred : {month}-{year}')
                            return None
                    else:
                        print(f'[*] Error {response.status} Occurred while fetching data for {month}-{year}')
                        return None
            except aiohttp.ClientConnectionError:
                if attempt < retries - 1:
                    print(f'[*] Connection error occurred. Retrying... Attempt {attempt + 1}/{retries}')
                    await asyncio.sleep(2)  # Wait before retrying
                else:
                    print('[*] Maximum retries reached. Unable to establish connection.')
                    return None

    async def main(self):
        tasks = []
        async with aiohttp.ClientSession() as session:
            current_year = datetime.datetime.now().year
            current_month = datetime.datetime.now().strftime('%b')
            current_month_index = MONTH.index(current_month)

            tasks = [
                self.fetch(session, year, month, url)
                for year in YEAR
                for month_index, month in enumerate(MONTH)
                for url in self.urls
                if not (int(year) > current_year or (int(year) == current_year and month_index > current_month_index))
            ]

            lotto_data = await asyncio.gather(*tasks)
            for data in lotto_data:
                if data is not None:
                    self.ParsedData.extend(data)



def add_lotto_data_to_db(session, lotto_data):

    for data in lotto_data:

        existing_result = session.query(Lotto_Result).filter_by(DrawDate=data['Date']).first()
        if existing_result:
            continue
        else:
                try:
                    DrawDate    = data['Date']
                    DrawNum     = data['Draw#']
                    Numbers     = data['Numbers']
                    Power_Ball  = data['Power Ball']
                    Multiplier  = data['Multiplier']
                    Jackpot     = data['Jackpot']
                    Wins        = data['Wins']
                    try:
                        DrawDate_str = DrawDate  # Date in string format
                        DrawDate = datetime.datetime.strptime(DrawDate_str, '%Y-%m-%d')  # Convert to date
                    except KeyError:
                        DrawDate = datetime.date(1990,1,1)

                    lotto_instance   = Lotto_Result(
                        DrawDate = DrawDate,
                        DrawNum = DrawNum,
                        Numbers = Numbers,
                        Power_Ball = Power_Ball,
                        Multiplier = Multiplier,
                        Jackpot = Jackpot,
                        Wins = Wins,
                    )

                    session.add(lotto_instance)
                except Exception as e:
                    print('[*] Error:', e)
    session.commit()

def generate_html_report(basic_analysis_report, additional_analysis_report, latest_entry, common_numbers, average_jackpot):
    # Format average jackpot as cash value
    average_jackpot_cash = "${:,.2f}".format(average_jackpot)

    # Split numbers drawn and format them
    numbers_drawn_list = latest_entry['Numbers'].split("-")
    numbers_drawn_formatted = ", ".join(numbers_drawn_list)



    # Generate HTML for most common numbers table
    most_common_numbers_html = ""
    for number, frequency in common_numbers:
        most_common_numbers_html += "<tr><td>{}</td><td>{}</td></tr>".format(number, frequency)

    basic = basic_analysis_report.replace("\n", "<br>")
    additional = additional_analysis_report.replace("\n", "<br>")


    ## Latest Entry Data
    DrawDate = datetime.datetime.strptime(latest_entry['Date'],"%Y-%m-%d").strftime("%d %B %Y")
    html_report = f"""<h1>Lottery Analysis Report</h1>
            <div class="basic-analysis">
                <h2>Basic Analysis:</h2>
                <p>{basic}</p>
            </div>
            <div class="average-jackpot">
                <h2>Average Jackpot Amount:</h2>
                <p>{average_jackpot_cash}</p>
            </div>
            <div class="most-common-numbers">
                <h3>Top 5 Most Common Numbers Drawn:</h3>
                <table>
                    <tr>
                        <th>Number</th>
                        <th>Frequency</th>
                    </tr>
                    {most_common_numbers_html}
                </table>
            </div>
            <div class="additional-analysis">
                <h2>Latest NLCB Lotto Plus Results:</h2>
                <div class="draw-date">
                    <h3>Draw Date:</h3>
                    <p>{DrawDate}</p>
                </div>
                <div class="numbers-drawn">
                    <h3>Numbers Drawn:</h3>
                    <p>{numbers_drawn_formatted}</p>
                </div>
                <br/>
                <h3>Other Information:</h3>
                <p>{additional}</p>

            </div>


        """
    return html_report

async def run_scraper(urls, db_session):
    scraper = WebScraper(urls)
    await scraper.main()
    add_lotto_data_to_db(db_session, scraper.ParsedData)

    # Perform basic analysis
    total_draws = len(scraper.ParsedData)
    try:
        average_jackpot = sum(float(result['Jackpot']) for result in scraper.ParsedData) / total_draws
    except Exception as e:
        average_jackpot = 0.0

    # Extract all numbers drawn
    all_numbers = [result['Numbers'].split("-") for result in scraper.ParsedData]
    flat_numbers = [int(number) for sublist in all_numbers for number in sublist]

    # Calculate the frequency of each number
    number_counts = pd.Series(flat_numbers).value_counts()

    # Find the most common numbers drawn
    most_common_numbers = number_counts.head(5)

    # Generate basic analysis report

    basic_analysis_report = f"Total number of draws: {total_draws}\n"
    common_numbers = []
    for number, count in most_common_numbers.items():
        common_numbers.append((number, f"{count} times\n"))

    # Perform additional analysis
    additional_analysis_report, latest_entry = additional_analysis(scraper.ParsedData)

    # Generate HTML report
    html_report = generate_html_report(basic_analysis_report, additional_analysis_report, latest_entry, common_numbers, average_jackpot)

    # Write HTML report to file
    with open('analysis_report.html', 'w') as file:
        file.write(html_report)

    print("Analysis reports generated successfully.")

def additional_analysis(data):
      # Get the latest entry
    latest_entry = data[-1] if data else None

    # Generate analysis report
    analysis_report = ""
    if latest_entry:
        analysis_report += f"Power Ball: {latest_entry['Power Ball']}\n"
        analysis_report += f"Multiplier: {latest_entry['Multiplier']}\n"
        analysis_report += f"Jackpot: {latest_entry['Jackpot']}\n"
        analysis_report += f"Wins: {latest_entry['Wins']}\n"
    else:
        analysis_report += "- No data available.\n"
        latest_entry = None
    return analysis_report, latest_entry

if __name__ == "__main__":
    start = perf_counter()
    urls = ['http://www.nlcbplaywhelotto.com/nlcb-lotto-plus-results/']
    engine = create_engine(f'sqlite:///{Database}',  echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    db_session = Session()
    try:
        asyncio.run(run_scraper(urls, db_session))
        print('[*] Adding Data to Database ... ')

    except IndentationError as e:
        print('*'*100)
        print(f'Error Occurred : {e}')
        print('*'*100)
    finally:
        db_session.close()

    stop = perf_counter()
    print("[*] Time taken : ", stop - start)
