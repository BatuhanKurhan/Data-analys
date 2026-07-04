#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 19:49:04 2026

@author: batuhankurhan
"""

import pandas as pd

df = pd.read_excel("/Users/batuhankurhan/Desktop/Trabzon_Ev_Fiyat_Tahmini/Trabzon_Konut.xlsx")

df["Metrekare"] = (
    df["Metrekare"]
    .astype(str)
    .str.replace(" m²", "", regex=False)
    .str.replace(".", "", regex=False)   # binlik ayıracı kaldır
    .str.strip()
)

df["Metrekare"] = pd.to_numeric(
    df["Metrekare"],
    errors="coerce"
)

df["Yas"] = (
    df["Yas"]
    .replace("Sıfır Bina", "0")
    .str.extract(r"(\d+)")
)

df["Yas"] = pd.to_numeric(df["Yas"], errors="coerce")

kat_map = {
    "Bahçe Katı": 0,
    "Giriş Katı": 0,
    "Yüksek Giriş": 0,
    "Zemin": 0,
    "Ara Kat": 3,
    "Villa Katı": 1,
    "Yarı Bodrum": -1,
    "Bodrum": -1,
    "Çatı Katı": 99,
    "En Üst Kat": 99
}

df["KatSayisi"] = df["Kat"].replace(kat_map)

mask = df["KatSayisi"].astype(str).str.contains(r"\d")

df.loc[mask, "KatSayisi"] = (
    df.loc[mask, "KatSayisi"]
      .astype(str)
      .str.extract(r"(\d+)", expand=False)
)

df["KatSayisi"] = pd.to_numeric(df["KatSayisi"])

df["Fiyat"] = (
    df["Fiyat"]
    .str.replace(".", "", regex=False)
    .str.replace(" TL", "", regex=False)
    .astype(int)
)

df["Ilce"] = df["Lokasyon"].str.split("/").str[1].str.strip()

df.to_csv(
    "trabzon_konut_temiz.csv",
    index=False,
    encoding="utf-8-sig"
)


