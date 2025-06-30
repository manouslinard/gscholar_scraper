import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

# Define your parameters ==
url = "https://scholar.google.com/citations?view_op=top_venues&hl=en&vq=eng_computervisionpatternrecognition"
file_xlsx = 'scholar_cv.xlsx'
wait_time = 5
# =========================

def scrape_subtable(table, venue_name):
    # Extract the titles and URLs
    titles_urls = []
    rows = table.find_all('tr')[1:]
    for row in rows:  # Skip the header row
        title_cell = row.find('td', {'class': 'gsc_mpat_t'})
        title = title_cell.find('a', {'class': 'gsc_mp_anchor_lrge'}).text
        url = "https://scholar.google.com" + title_cell.find('a', {'class': 'gsc_mp_anchor_lrge'})['href']

        citation_cell = row.find('td', {'class': 'gsc_mpat_c'})
        citations = citation_cell.text.strip()
        
        year_cell = row.find('td', {'class': 'gsc_mpat_y'})
        year = year_cell.text.strip()

        author_cell = title_cell.find('div', {'class': 'gs_gray'})
        authors = author_cell.text if author_cell else "N/A"
        titles_urls.append((venue_name, title, url, authors, citations, year))

    return titles_urls

# create Chrome options (no tab):
try:
    options = Options()
    options.add_argument('--headless')  # remove this if you want the browser to appear.
    # create Chrome service - installs chrome driver:
    service = Service(ChromeDriverManager().install())
    # initialise driver:
    driver = webdriver.Chrome(service=service, options=options)
except: # starts firefox    
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')  # remove this if you want the browser to appear.
    service = webdriver.firefox.service.Service(executable_path=GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)# go to url:

driver.get(url)
html_content = driver.page_source

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')
# print(soup.prettify()) 

# Find the table containing the venues
table = soup.find('table', {'id': 'gsc_mvt_table'})

# Initialize a list to store the extracted data
venues = []

# Check if the table exists
if table:
    # Iterate over each row in the table
    for row in table.find_all('tr'):
        columns = row.find_all('td')
        if len(columns) > 1:
            venue_name = columns[1].text.strip()
            h5_index_url = columns[2].find('a')['href'] if columns[2].find('a') else ''
            full_h5_index_url = f"https://scholar.google.com{h5_index_url}"
            venues.append([venue_name, full_h5_index_url])

time.sleep(wait_time)

df = pd.DataFrame(columns=['Venue Name', 'Article Title', 'URL', 'Authors', 'Citations', 'Year'])
for v in venues:
    v_name = v[0]
    v_url = v[1]
    d = []
    c_start = 0
    print(f"Scraping for venue: {v_name}")
    while True:
        driver.get(v_url + f'&cstart={c_start}')
        html_content = driver.page_source
        c_start += 20
        soup = BeautifulSoup(html_content, 'html.parser')
        try:
            table = soup.find('table', {'id': 'gsc_mpat_table'})
            if table:
                data = scrape_subtable(table, v_name)
                if len(data) <= 0:
                    break
                print(f"Papers Range: {c_start} -> {c_start + len(data)}")
                df = df._append(pd.DataFrame(data, columns=['Venue Name', 'Article Title', 'URL', 'Authors', 'Citations', 'Year']), ignore_index=True)
            else:
                break
        except AttributeError:
            # print("Table with ID 'gsc_mpat_table' not found.")
            break
        time.sleep(2*wait_time)
        # print(df)
        df.to_excel(file_xlsx, index=False)
    # break

