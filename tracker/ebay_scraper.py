import asyncio
import pandas as pd
from playwright.async_api import async_playwright

async def scrape_ebay(search_term):
    url = f"https://www.ebay.com/sch/i.html?_nkw={search_term.replace(' ', '+')}&_sop=12"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_user_agent("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
        
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            await asyncio.sleep(5)  # give time for JS to load listings
            await page.screenshot(path=f"{search_term.replace(' ', '_')}_debug.png", full_page=True)

            titles = await page.locator("li.s-item h3.s-item__title").all_inner_texts()
            prices = await page.locator("li.s-item span.s-item__price").all_inner_texts()

            print(f"[{search_term}] Found {len(titles)} listings")
            return [{"search_term": search_term, "title": t, "price": p} for t, p in zip(titles, prices)]

        except Exception as e:
            print(f"Error scraping {search_term}: {e}")
            return []

        finally:
            await browser.close()

async def main():
    search_terms = ["adidas samba", "adidas gazelle", "adidas sl72"]
    all_results = []

    for term in search_terms:
        listings = await scrape_ebay(term)
        all_results.extend(listings)

    df = pd.DataFrame(all_results)
    print("\nSample Listings:")
    print(df.head())

    df.to_csv("ebay_results.csv", index=False)
    print("\nSaved eBay listings to 'ebay_results.csv'")

if __name__ == "__main__":
    asyncio.run(main())
