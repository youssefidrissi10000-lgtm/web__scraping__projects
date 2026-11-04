# Avito Laptops Scraper

Helps you compare gaming laptop prices on Avito.ma without browsing page by page.

- Script: [scraper.py](scraper.py)
- Result: [avito_laptops.csv](avito_laptops.csv)

## Tools
- Python
- Playwright
- pandas

## How to run
1. Install the libraries: pip install pandas playwright
2. Install the browser: playwright install chromium
3. Run the script: python scraper.py

## Output
The script saves the results in avito_laptops.csv with 3 columns:
- tatle: the laptop title
- price_dh: the price in DH
- lien_prodwe: the link to the listing