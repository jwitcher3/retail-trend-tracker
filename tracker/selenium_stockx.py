# StockX Scraper using Selenium (Headless) with Price Data for Multiple Franchises and Sort by Total Sold

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd

def scrape_stockx_data(search_term):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)

    # Updated URL with sort by Total Sold
    url = f"https://stockx.com/search?s={search_term.replace(' ', '%20')}&sort=deadstock_sold"
    driver.get(url)
    time.sleep(10)  # wait for JS to load

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    titles = soup.select("p[data-testid='product-tile-title']")
    prices = soup.select("p[data-testid='product-tile-lowest-ask-amount']")

    print(f"[{search_term}] Found {len(titles)} titles and {len(prices)} lowest asks")

    results = []
    for title_tag, price_tag in zip(titles, prices):
        title = title_tag.text.strip()
        price = price_tag.text.strip()
        results.append({"franchise": search_term, "title": title, "lowest_ask": price})

    driver.quit()
    return results

if __name__ == "__main__":
    franchises = ["Samba", "Gazelle", "SL72"]
    all_results = []

    for franchise in franchises:
        franchise_results = scrape_stockx_data(franchise)
        all_results.extend(franchise_results)

    df = pd.DataFrame(all_results)
    print("\nCombined Results:")
    print(df.head())

        # Save to CSV
    df.to_csv("stockx_combined_results.csv", index=False)
    print("\nSaved results to 'stockx_combined_results.csv'")
