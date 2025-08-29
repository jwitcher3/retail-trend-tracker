# GOAT Scraper using Undetected ChromeDriver (Stealth Headless)

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

def scrape_goat_data(search_term):
    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = uc.Chrome(options=options)

    url = f"https://www.goat.com/search?query={search_term.replace(' ', '%20')}"
    driver.get(url)
    time.sleep(10)

    # Scroll down to load lazy-loaded content
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    titles = [tag.text.strip() for tag in soup.select("div[data-qa='grid_cell_product_name']")]
    prices = [tag.text.strip() for tag in soup.select("div[data-qa='grid_cell_price']")]

    print(f"[{search_term}] Found {len(titles)} titles and {len(prices)} prices")

    results = []
    for title, price in zip(titles, prices):
        results.append({"franchise": search_term, "title": title, "price": price})

    driver.quit()
    return results

if __name__ == "__main__":
    franchises = ["Samba", "Gazelle", "SL72"]
    all_results = []

    for franchise in franchises:
        franchise_results = scrape_goat_data(franchise)
        all_results.extend(franchise_results)

    df = pd.DataFrame(all_results)
    print("\nCombined GOAT Results:")
    print(df.head())

    # Save to CSV
    df.to_csv("goat_combined_results.csv", index=False)
    print("\nSaved results to 'goat_combined_results.csv'")
