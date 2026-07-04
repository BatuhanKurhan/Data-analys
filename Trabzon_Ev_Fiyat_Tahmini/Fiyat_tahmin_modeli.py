#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 20:10:54 2026

@author: batuhankurhan
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score


df=pd.read_csv("/Users/batuhankurhan/Desktop/Trabzon_Ev_Fiyat_Tahmini/trabzon_konut_temiz.csv")

#Gereksiz sütunları sildim. 
df_yeni = df.drop(
    ["Link", "Baslik","KatSayisi","Lokasyon"],
    axis=1
)

#Eksik verileri doldurdum.
df_yeni["Kat"] = df_yeni["Kat"].fillna("Bilinmiyor")


#Aykırı değerleri görmek için kutu grafiği çizdirdim.
plt.boxplot(df_yeni["Fiyat"])
plt.title("Fiyat")
plt.show()

plt.boxplot(df_yeni["Yas"])
plt.title("Yas")
plt.show()

plt.boxplot(df_yeni["Metrekare"])
plt.title("Metrekare")
plt.show()

#Aykırı değerleri sildim.
sayisal_sutunlar = [
    "Metrekare",
    "Yas"
]

for col in sayisal_sutunlar:

    Q1 = df_yeni[col].quantile(0.25)
    Q3 = df_yeni[col].quantile(0.75)

    IQR = Q3 - Q1

    alt = Q1 - 1.5 * IQR
    ust = Q3 + 1.5 * IQR

    df_yeni = df_yeni[
        (df_yeni[col] >= alt) &
        (df_yeni[col] <= ust)
    ]


#Fiyatlar için log dönüşümü yaptım.
df["LogFiyat"] = np.log1p(df["Fiyat"])


#Hedef değişkeni belirledim.
X=df_yeni.drop("Fiyat",axis=1)
y=df_yeni["Fiyat"]

#Kategorik verileri belirledim.
categorical_features = ["Kat","Ilce"]

#OneHotEncoder ile kategorik verileri işlenebilir hale getirdim.
preprocessor = ColumnTransformer(
    transformers=[
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ],
    remainder="passthrough"
)

#Modeli kurdum

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),

        ("regressor",
         RandomForestRegressor(
             n_estimators=250,
             random_state=42
         ))
    ]
)

#Eğitim ve test verisini böldüm.
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

#Model eğitimi.
model.fit(X_train,y_train)


#Tahmin
y_pred = model.predict(X_test)

#Modelin performans ölçütleri
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5
r2 = r2_score(y_test, y_pred)

print("===== MODEL PERFORMANSI =====")
print(f"MAE  : {mae:,.2f} TL")
print(f"MSE  : {mse:,.2f}")
print(f"RMSE : {rmse:,.2f} TL")
print(f"R²   : {r2:.4f}")




















