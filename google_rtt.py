# Retail Trend Tracker (Google Trends Version)

# Purpose: Track Google Trends interest for key sneaker/apparel franchises and fashion trends
# Goal: Surface emerging product and franchise signals for weekly monitoring in US and Canada

from pytrends.request import TrendReq
import numpy as np
import pandas as pd
import datetime
from time import sleep
import plotly.express as px
import os

# --- SETUP ---
sneaker_franchises = ["Samba", "Gazelle", "Air Force 1", "New Balance 550", "Salomon XT-6"]
fashion_keywords = [
    "baggy jeans", "chunky sneakers", "cargo pants", "cropped tops", "puffer jackets",
    "athleisure", "quiet luxury", "gorpcore", "Y2K fashion", "normcore"
]

# --- FETCH TRENDS IN BATCHES ---
def fetch_trends_batched(keywords, country_code, timeframe='today 3-m'):
    pytrends = TrendReq(hl='en-US', tz=360)
    batched_data = []

    for i in range(0, len(keywords), 5):
        group = keywords[i:i+5]
        try:
            pytrends.build_payload(group, cat=0, timeframe=timeframe, geo=country_code, gprop='')
            df = pytrends.interest_over_time().reset_index()
            df['country'] = country_code
            batched_data.append(df)
            sleep(1)
        except Exception as e:
            print(f"Batch failed for {group}: {e}")

    final_df = pd.concat(batched_data, axis=0, ignore_index=True)
    return final_df

# --- INTERACTIVE VISUALIZATION ---
def plot_trends_interactive(df, title):
    melted = df.melt(id_vars=['date'], value_vars=[col for col in df.columns if col not in ['date', 'isPartial', 'country']], var_name='trend', value_name='interest')
    fig = px.line(melted, x='date', y='interest', color='trend', title=title)
    fig.update_layout(xaxis_title='Date', yaxis_title='Google Trends Interest')
    fig.show()

# --- MAIN ---
if __name__ == "__main__":
    # Sneaker trends
    us_sneaker_df = fetch_trends_batched(sneaker_franchises, 'US')
    ca_sneaker_df = fetch_trends_batched(sneaker_franchises, 'CA')

    # Fashion trends
    us_fashion_df = fetch_trends_batched(fashion_keywords, 'US')
    ca_fashion_df = fetch_trends_batched(fashion_keywords, 'CA')

    # Export all trends to CSV
    all_trends_df = pd.concat([
        us_sneaker_df.assign(segment="Sneakers", region="US"),
        ca_sneaker_df.assign(segment="Sneakers", region="CA"),
        us_fashion_df.assign(segment="Fashion", region="US"),
        ca_fashion_df.assign(segment="Fashion", region="CA")
    ])
    all_trends_df.to_csv("trends.csv", index=False)

    # Interactive visuals
    print("\nUS Sneaker Trends:")
    plot_trends_interactive(us_sneaker_df, "US Sneaker Trends (Google Trends)")
    print("\nCanada Sneaker Trends:")
    plot_trends_interactive(ca_sneaker_df, "Canada Sneaker Trends (Google Trends)")

    print("\nUS Fashion Trends:")
    plot_trends_interactive(us_fashion_df, "US Fashion Trends (Google Trends)")
    print("\nCanada Fashion Trends:")
    plot_trends_interactive(ca_fashion_df, "Canada Fashion Trends (Google Trends)")
