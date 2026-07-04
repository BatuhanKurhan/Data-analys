from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)

all_data = []

for page in range(1, 20):

    url = f"https://www.hepsiemlak.com/trabzon-satilik?p33=1&page={page}&p31=700000"

    print(f"Sayfa {page} okunuyor...")

    driver.get(url)

    time.sleep(5)

    cards = driver.find_elements(
        By.CSS_SELECTOR,
        "a.listingView__card-link"
    )

    print(f"{len(cards)} ilan bulundu.")

    for card in cards:

        try:

            title = ""

            try:
                title = card.find_element(
                    By.CSS_SELECTOR,
                    "h3"
                ).text
            except:
                pass

            try:
                price = card.find_element(
                    By.CSS_SELECTOR,
                    ".list-view-price"
                ).text
            except:
                price = ""

            try:
                location = card.find_element(
                    By.CSS_SELECTOR,
                    "address"
                ).text
            except:
                location = ""

            try:
                age = card.find_element(
                    By.CSS_SELECTOR,
                    ".buildingAge"
                ).text
            except:
                age = ""

            try:
                floor = card.find_element(
                    By.CSS_SELECTOR,
                    ".floortype"
                ).text
            except:
                floor = ""

            try:
                square_meter = card.find_element(
                    By.CSS_SELECTOR,
                    ".squareMeter"
                ).text
            except:
                square_meter = ""

            try:
                link = card.get_attribute("href")
            except:
                link = ""

            all_data.append({
                "Baslik": title,
                "Fiyat": price,
                "Lokasyon": location,
                "Yas": age,
                "Kat": floor,
                "Metrekare": square_meter,
                "Link": link
            })

        except Exception as e:
            print("Hata:", e)

driver.quit()

df = pd.DataFrame(all_data)

print(f"\nToplam {len(df)} ilan çekildi.")

df.to_excel(
    "trabzon_konut.xlsx",
    index=False
)

print("Excel dosyası oluşturuldu: trabzon_satilik_konut.xlsx")