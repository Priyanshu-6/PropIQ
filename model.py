# house_price_model.py
# Dependencies:
# pip install streamlit scikit-learn pandas numpy joblib matplotlib plotly india-housing-datasets

import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

from india_housing_datasets import load_housing
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor


def main():

    # Load dataset
    df = load_housing("chandigarh")

    print("First 5 rows:\n", df.head())
    print("Last 5 rows:\n", df.tail())
    print("Dataset shape:", df.shape)

    # Remove missing values
    df = df.dropna()
    print("Rows after dropping missing values:", len(df))

    # Save original locality names BEFORE encoding (needed for Similar Properties feature in app.py)
    df_with_names = df.copy()
    df_with_names = df_with_names.drop("city", axis=1)
    df_with_names.to_csv("housing_data.csv", index=False)
    print("Raw dataset (with locality names) saved to housing_data.csv ✅")

    # Encode locality column
    le = LabelEncoder()
    df['locality'] = le.fit_transform(df['locality'])

    # Drop city column
    df = df.drop("city", axis=1)

    print("\nDataset preview after preprocessing:\n", df.head())

    # Feature selection
    X = df.drop("price_lakhs", axis=1)
    y = df["price_lakhs"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train Random Forest model (primary)
    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("\nRandom Forest Evaluation:")
    print("R2 Score:", model.score(X_test, y_test))
    print("MAE:", mean_absolute_error(y_test, y_pred))
    print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))

    # Train multiple models for comparison
    lr = LinearRegression()
    dt = DecisionTreeRegressor(random_state=42)
    rf = RandomForestRegressor(random_state=42)

    lr.fit(X_train, y_train)
    dt.fit(X_train, y_train)
    rf.fit(X_train, y_train)

    # Model scores
    lr_score = lr.score(X_test, y_test)
    dt_score = dt.score(X_test, y_test)
    rf_score = rf.score(X_test, y_test)

    print("\nModel Comparison:")
    print("Linear Regression Score:", lr_score)
    print("Decision Tree Score:", dt_score)
    print("Random Forest Score:", rf_score)

    # Save best model and encoder
    best_model = rf
    joblib.dump(best_model, "house_price_model.pkl")
    joblib.dump(le, "locality_encoder.pkl")

    print("\nModel and encoder saved successfully ✅")


if __name__ == "__main__":
    main() 