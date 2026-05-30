#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 30 17:00:25 2026

@author: batuhankurhan
"""

import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Loading data

df = sns.load_dataset("titanic")


# Fill in missing data

df["age"] = df["age"].fillna(df["age"].median())
df['is_child'] = (df['age'] < 16).astype(int)

# Encoding

df["sex"] = df["sex"].map({"male":0 , "female":1})

# Pre-processing

features = ["survived","pclass","sex","age","fare","is_child"]
df = df[features].copy()


# Target
X=df.drop("survived",axis=1)
y=df["survived"]

# Split
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)

# Training

model = RandomForestClassifier(n_estimators=500,max_depth=8,random_state=42)
model.fit(X_train,y_train)

# Metrics

y_pred = model.predict(X_test)
acuucaracy = accuracy_score(y_test , y_pred)

print("Model Doğruluğu (Accuracy):",acuucaracy)
print("Sınıflandırma Raporu (Classification Report):")
print(classification_report(y_test, y_pred, target_names=["Öldü (0)", "Kurtuldu (1)"]))









