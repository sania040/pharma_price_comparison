import os
from bs4 import BeautifulSoup
import pandas as pd

HTML_FOLDER = "./html_files"

def extract_medicine_prices(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f, "html.parser")
    data = []
    rows = soup.find_all("tr", class_="item")
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 3:
            code = cols[0].get_text(strip=True)
            name = cols[1].get_text(strip=True).upper()
            try:
                price = float(cols[2].get_text(strip=True))
            except ValueError:
                continue
            data.append((code, name, price))
    return data

def load_all_data():
    combined = []
    for file in os.listdir(HTML_FOLDER):
        if file.endswith(".htm") or file.endswith(".html"):
            full_path = os.path.join(HTML_FOLDER, file)
            data = extract_medicine_prices(full_path)
            for code, name, price in data:
                combined.append({
                    "Medicine Code": code,
                    "Medicine Name": name,
                    "Price": price,
                    "File": file
                })
    return pd.DataFrame(combined)

def search_medicine(medicine_name, df):
    search = medicine_name.strip().upper()
    results = df[df["Medicine Name"].str.contains(search)]
    if results.empty:
        print(f"No results found for '{medicine_name}'.")
        return
    print("\nAll available prices:\n")
    print(results.sort_values(by="Price"))
    min_row = results.loc[results["Price"].idxmin()]
    print("\n💡 Lowest Price:")
    print(f"{min_row['Price']} in file: {min_row['File']}")

if __name__ == "__main__":
    df = load_all_data()
    while True:
        med = input("\n🔍 Enter medicine name to search (or type 'exit' to quit): ").strip()
        if med.lower() == "exit":
            break
        search_medicine(med, df)
