# Changelog

All notable changes to PropIQ will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] — 2026-05-01

### 🎉 Initial Public Release

This is the first open source release of PropIQ — an AI-powered house price predictor for the Chandigarh Tri-City region.

### Added
- 🎯 **Price Prediction Engine** — Random Forest Regressor trained on Chandigarh housing data
- 📊 **95% Confidence Interval** — price range calculated from all 100 individual decision trees
- 🏘️ **Similar Properties Module** — top 5 comparable listings ranked by locality, BHK, and area
- 📈 **Market Trend Visualisations** — average price by top 15 localities and by BHK type
- 🔄 **What-If Sensitivity Analysis** — price elasticity charts for area (±500 sqft) and BHK variations
- 🏦 **EMI & Affordability Calculator** — monthly EMI, total interest, and donut chart breakdown
- 🎨 **Dark-mode Streamlit UI** — custom CSS with gradient cards, metric displays, and Plotly charts
- ☁️ **Streamlit Community Cloud deployment** — publicly accessible live demo
- 📄 **MIT License** — fully open source
- 🤝 **Contributing guidelines** — CONTRIBUTING.md and CODE_OF_CONDUCT.md
- 🐛 **GitHub Issue Templates** — Bug Report and Feature Request templates

### Tech Stack
- Python, Streamlit, scikit-learn, pandas, numpy, joblib, Plotly
- Data: india-housing-datasets library (Chandigarh region)

---

## How to Read This File

- **Added** — new features
- **Changed** — changes to existing features
- **Fixed** — bug fixes
- **Removed** — removed features
- **Security** — security patches