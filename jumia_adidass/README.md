# Jumia Price Alert

Tracks Adidas product prices on Jumia.ma and emails you when prices drop, so you never check the website by hand.

- Script: [scraper.py](scraper.py)
- Result: [adidass_result.csv](adidass_result.csv)

## What it does
1. Collects products from 3 pages of Jumia.
2. Cleans the data (removes duplicates and empty rows, converts prices to numbers).
3. Filters products at or below your price limit.
4. Sends an email alert with the number of products, plus the full report attached.
5. Runs automatically every day at 09:00.

## Tools
- Python
- Playwright
- pandas
- smtplib
- schedule

## How to run
1. Install the libraries: pip install pandas playwright schedule python-dotenv openpyxl
2. Install the browser: playwright install chromium
3. Create a .env file with GMAIL, GMAIL_TO and GMAIL_PASSWORD (your Gmail App Password)
4. Run the script: python scraper.py

## Output
The script saves the results in adidass_result.csv with 3 columns:
- tatle: the product title
- prex: the price in DH
- lenc_adidas: the link to the product