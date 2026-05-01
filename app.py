# app.py — Enhanced House Price Predictor (Chandigarh / Tri-City)
# Run with: streamlit run app.py

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go

from india_housing_datasets import load_housing

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PropIQ — House Price Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0f1117; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1f2e 0%, #16213e 100%);
        border-right: 1px solid #2d3561;
    }

    /* Cards */
    .metric-card {
        background: linear-gradient(135deg, #1e2a45 0%, #16213e 100%);
        border: 1px solid #2d3561;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 10px;
    }
    .metric-card h2 {
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        background: linear-gradient(90deg, #4facfe, #00f2fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card p {
        color: #8892b0;
        margin: 4px 0 0 0;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Section headers */
    .section-header {
        color: #4facfe;
        font-size: 1.1rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        border-bottom: 2px solid #2d3561;
        padding-bottom: 8px;
        margin-bottom: 16px;
    }

    /* Prediction box */
    .prediction-box {
        background: linear-gradient(135deg, #0f3460 0%, #16213e 100%);
        border: 2px solid #4facfe;
        border-radius: 16px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 0 30px rgba(79, 172, 254, 0.15);
    }
    .prediction-box .price {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #4facfe, #00f2fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .prediction-box .range {
        color: #8892b0;
        font-size: 1rem;
        margin-top: 8px;
    }

    /* EMI box */
    .emi-box {
        background: linear-gradient(135deg, #1a1f2e 0%, #0f1117 100%);
        border: 1px solid #2d3561;
        border-radius: 12px;
        padding: 20px;
    }

    /* Table styling */
    .stDataFrame { border-radius: 10px; overflow: hidden; }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #4facfe, #00f2fe) !important;
        color: #0f1117 !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        padding: 12px 30px !important;
        width: 100% !important;
        font-size: 1rem !important;
        letter-spacing: 0.5px;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(79, 172, 254, 0.4) !important;
    }

    /* Slider */
    .stSlider > div > div > div { background: #4facfe !important; }

    /* Input labels */
    label { color: #ccd6f6 !important; font-size: 0.9rem !important; }

    /* Number input */
    .stNumberInput input { background: #1a1f2e !important; color: #e6f1ff !important; border: 1px solid #2d3561 !important; border-radius: 8px !important; }

    /* Select box */
    .stSelectbox > div > div { background: #1a1f2e !important; color: #e6f1ff !important; border: 1px solid #2d3561 !important; border-radius: 8px !important; }

    /* Divider */
    hr { border-color: #2d3561 !important; }

    /* Info / warning */
    .stInfo { background: rgba(79, 172, 254, 0.1) !important; border: 1px solid rgba(79, 172, 254, 0.3) !important; border-radius: 8px !important; }
</style>
""", unsafe_allow_html=True)


# ─── Load Model & Data ────────────────────────────────────────────────────────
@st.cache_resource
def load_model_and_encoder():
    model = joblib.load("house_price_model.pkl")
    le = joblib.load("locality_encoder.pkl")
    return model, le

@st.cache_data
def load_dataset():
    try:
        # Try loading from the saved CSV first (has original locality names)
        df = pd.read_csv("housing_data.csv")
    except FileNotFoundError:
        # Fallback: load from the library directly
        df = load_housing("chandigarh")
        df = df.dropna()
        if "city" in df.columns:
            df = df.drop("city", axis=1)
    return df

model, le = load_model_and_encoder()
df_raw = load_dataset()
locality_list = sorted(df_raw["locality"].unique())


# ─── Sidebar — Inputs ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏠 House Details")
    st.markdown("---")

    st.markdown('<p class="section-header">📐 Property Info</p>', unsafe_allow_html=True)

    area = st.number_input("Area (sqft)", min_value=100, max_value=10000, value=1000, step=50)
    bhk = st.number_input("BHK", min_value=1, max_value=10, value=2, step=1)
    bath = st.number_input("Bathrooms", min_value=1, max_value=10, value=2, step=1)
    floor = st.number_input("Floor Number", min_value=0, max_value=50, value=1, step=1)
    age = st.number_input("House Age (years)", min_value=0, max_value=100, value=5, step=1)

    st.markdown("---")
    st.markdown('<p class="section-header">📍 Location</p>', unsafe_allow_html=True)
    locality = st.selectbox("Select Locality", locality_list)

    st.markdown("---")
    st.markdown('<p class="section-header">🏦 Loan Details</p>', unsafe_allow_html=True)
    down_payment_pct = st.slider("Down Payment (%)", min_value=5, max_value=50, value=20, step=5)
    loan_tenure = st.slider("Loan Tenure (years)", min_value=5, max_value=30, value=20, step=5)
    interest_rate = st.slider("Interest Rate (% p.a.)", min_value=6.0, max_value=15.0, value=8.5, step=0.25)

    st.markdown("---")
    predict_btn = st.button("🔍 Predict Price")


# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("# 🏠 PropIQ — Tri-City House Price Predictor")
st.markdown("**Chandigarh · Mohali · Panchkula** — AI-powered real estate insights")
st.markdown("---")


# ─── Default State: Market Overview ──────────────────────────────────────────
if not predict_btn:

    st.markdown("### 📊 Market Overview — Chandigarh Region")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        avg_price = df_raw["price_lakhs"].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h2>₹{avg_price:.1f}L</h2>
            <p>Avg Price</p>
        </div>""", unsafe_allow_html=True)

    with col2:
        median_price = df_raw["price_lakhs"].median()
        st.markdown(f"""
        <div class="metric-card">
            <h2>₹{median_price:.1f}L</h2>
            <p>Median Price</p>
        </div>""", unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h2>{len(df_raw)}</h2>
            <p>Listings</p>
        </div>""", unsafe_allow_html=True)

    with col4:
        num_localities = df_raw["locality"].nunique()
        st.markdown(f"""
        <div class="metric-card">
            <h2>{num_localities}</h2>
            <p>Localities</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── Feature 3: Price Trend by Locality ────────────────────────────────────
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### 📍 Avg Price by Locality (Top 15)")
        locality_avg = (
            df_raw.groupby("locality")["price_lakhs"]
            .mean()
            .sort_values(ascending=False)
            .head(15)
            .reset_index()
        )
        fig1 = px.bar(
            locality_avg,
            x="price_lakhs",
            y="locality",
            orientation="h",
            color="price_lakhs",
            color_continuous_scale="Blues",
            labels={"price_lakhs": "Avg Price (Lakhs)", "locality": "Locality"},
        )
        fig1.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#ccd6f6",
            coloraxis_showscale=False,
            margin=dict(l=10, r=10, t=10, b=10),
            height=380,
        )
        fig1.update_xaxes(gridcolor="#2d3561", zerolinecolor="#2d3561")
        fig1.update_yaxes(gridcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig1, use_container_width=True)

    with col_right:
        st.markdown("#### 🛏️ Avg Price by BHK Type")
        bhk_avg = (
            df_raw.groupby("bhk")["price_lakhs"]
            .mean()
            .reset_index()
            .rename(columns={"bhk": "BHK", "price_lakhs": "Avg Price (Lakhs)"})
        )
        fig2 = px.bar(
            bhk_avg,
            x="BHK",
            y="Avg Price (Lakhs)",
            color="Avg Price (Lakhs)",
            color_continuous_scale="Teal",
            text_auto=".1f",
        )
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#ccd6f6",
            coloraxis_showscale=False,
            margin=dict(l=10, r=10, t=10, b=10),
            height=380,
        )
        fig2.update_xaxes(gridcolor="#2d3561", zerolinecolor="#2d3561")
        fig2.update_yaxes(gridcolor="#2d3561")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.info("👈 Fill in your property details in the sidebar and click **Predict Price** to get started.")


# ─── Prediction Results ───────────────────────────────────────────────────────
if predict_btn:

    locality_encoded = list(le.classes_).index(locality) if locality in list(le.classes_) else locality_list.index(locality)
    features = np.array([[area, bhk, bath, floor, age, locality_encoded]])

    # ── Feature 1: Confidence Interval ────────────────────────────────────────
    tree_predictions = np.array([tree.predict(features)[0] for tree in model.estimators_])
    mean_price = tree_predictions.mean()
    std_dev = tree_predictions.std()
    lower = max(0, mean_price - 1.96 * std_dev)
    upper = mean_price + 1.96 * std_dev

    # ─── Main Prediction Display ──────────────────────────────────────────────
    st.markdown(f"""
    <div class="prediction-box">
        <p style="color:#8892b0; font-size:0.9rem; text-transform:uppercase; letter-spacing:2px; margin-bottom:8px;">Estimated Price</p>
        <div class="price">₹{mean_price:.2f} Lakhs</div>
        <div class="range">📊 95% Confidence Range: ₹{lower:.2f}L — ₹{upper:.2f}L</div>
        <div style="color:#8892b0; font-size:0.8rem; margin-top:6px;">📍 {locality} | {int(bhk)} BHK | {int(area)} sqft</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Quick Stats Row ───────────────────────────────────────────────────────
    col1, col2, col3 = st.columns(3)
    price_per_sqft = (mean_price * 100000) / area if area > 0 else 0

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h2>₹{price_per_sqft:,.0f}</h2>
            <p>Per Sqft</p>
        </div>""", unsafe_allow_html=True)

    with col2:
        confidence_pct = max(0, 100 - (std_dev / mean_price * 100)) if mean_price > 0 else 0
        st.markdown(f"""
        <div class="metric-card">
            <h2>{confidence_pct:.0f}%</h2>
            <p>Model Confidence</p>
        </div>""", unsafe_allow_html=True)

    with col3:
        spread = upper - lower
        st.markdown(f"""
        <div class="metric-card">
            <h2>₹{spread:.1f}L</h2>
            <p>Price Spread</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── Feature 4: What-If Sensitivity Analysis ────────────────────────────────
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### 🔄 What-If: Area Sensitivity")
        area_range = np.arange(max(100, area - 500), area + 600, 100)
        prices_area = []
        for a in area_range:
            f = np.array([[a, bhk, bath, floor, age, locality_encoded]])
            prices_area.append(model.predict(f)[0])

        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=area_range, y=prices_area,
            mode="lines+markers",
            line=dict(color="#4facfe", width=3),
            marker=dict(size=6, color="#4facfe"),
            fill="tozeroy",
            fillcolor="rgba(79,172,254,0.08)",
            name="Predicted Price"
        ))
        fig3.add_vline(x=area, line_dash="dash", line_color="#00f2fe", annotation_text="Your Input")
        fig3.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#ccd6f6",
            xaxis_title="Area (sqft)",
            yaxis_title="Price (Lakhs)",
            margin=dict(l=10, r=10, t=10, b=10),
            height=300,
            showlegend=False,
        )
        fig3.update_xaxes(gridcolor="#2d3561")
        fig3.update_yaxes(gridcolor="#2d3561")
        st.plotly_chart(fig3, use_container_width=True)

    with col_right:
        st.markdown("#### 🔄 What-If: BHK Sensitivity")
        bhk_range = list(range(1, 7))
        prices_bhk = []
        for b in bhk_range:
            f = np.array([[area, b, bath, floor, age, locality_encoded]])
            prices_bhk.append(model.predict(f)[0])

        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            x=[f"{b} BHK" for b in bhk_range],
            y=prices_bhk,
            marker_color=["#4facfe" if b == int(bhk) else "#2d3561" for b in bhk_range],
            text=[f"₹{p:.1f}L" for p in prices_bhk],
            textposition="outside",
            textfont=dict(color="#ccd6f6"),
        ))
        fig4.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#ccd6f6",
            xaxis_title="BHK",
            yaxis_title="Price (Lakhs)",
            margin=dict(l=10, r=10, t=10, b=30),
            height=300,
        )
        fig4.update_xaxes(gridcolor="rgba(0,0,0,0)")
        fig4.update_yaxes(gridcolor="#2d3561")
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")

    # ── Feature 2: Similar Properties ─────────────────────────────────────────
    st.markdown("#### 🏘️ Similar Properties in the Market")

    similar = df_raw[df_raw["locality"] == locality].copy()

    if len(similar) == 0:
        similar = df_raw.copy()

    # Score by similarity (area ±30%, same BHK preferred)
    similar["area_diff"] = abs(similar["area_sqft"] - area)
    similar["bhk_match"] = (similar["bhk"] == bhk).astype(int)
    similar["score"] = similar["bhk_match"] * 10000 - similar["area_diff"]
    similar = similar.sort_values("score", ascending=False).head(5)

    display_cols = ["locality", "area_sqft", "bhk", "bath", "floor", "age", "price_lakhs"]
    display_cols = [c for c in display_cols if c in similar.columns]
    similar_display = similar[display_cols].copy()
    similar_display.columns = [c.replace("_", " ").title() for c in similar_display.columns]
    similar_display = similar_display.reset_index(drop=True)
    similar_display.index += 1

    st.dataframe(
        similar_display,
        use_container_width=True,
        hide_index=False,
    )

    st.markdown("---")

    # ── Feature 5: EMI Calculator ──────────────────────────────────────────────
    st.markdown("#### 🏦 EMI & Affordability Calculator")

    loan_amount_lakhs = mean_price * (1 - down_payment_pct / 100)
    loan_amount_rs = loan_amount_lakhs * 100000
    monthly_rate = interest_rate / (12 * 100)
    n_months = loan_tenure * 12

    if monthly_rate > 0:
        emi = (loan_amount_rs * monthly_rate * (1 + monthly_rate) ** n_months) / \
              ((1 + monthly_rate) ** n_months - 1)
    else:
        emi = loan_amount_rs / n_months

    total_payment = emi * n_months
    total_interest = total_payment - loan_amount_rs

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h2>₹{emi/1000:.1f}K</h2>
            <p>Monthly EMI</p>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h2>₹{loan_amount_lakhs:.1f}L</h2>
            <p>Loan Amount</p>
        </div>""", unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h2>₹{total_interest/100000:.1f}L</h2>
            <p>Total Interest</p>
        </div>""", unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h2>₹{total_payment/100000:.1f}L</h2>
            <p>Total Payment</p>
        </div>""", unsafe_allow_html=True)

    # Donut chart — Principal vs Interest
    fig5 = go.Figure(data=[go.Pie(
        labels=["Principal", "Interest"],
        values=[loan_amount_rs, total_interest],
        hole=0.65,
        marker=dict(colors=["#4facfe", "#ff6b6b"], line=dict(color="#0f1117", width=2)),
        textinfo="label+percent",
        textfont=dict(color="#ccd6f6"),
    )])
    fig5.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#ccd6f6",
        showlegend=False,
        height=250,
        margin=dict(l=10, r=10, t=10, b=10),
        annotations=[dict(
            text=f"₹{emi/1000:.1f}K<br>/month",
            x=0.5, y=0.5, font_size=16, showarrow=False,
            font=dict(color="#4facfe", family="Arial")
        )]
    )
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("---")
    st.markdown(
        "<p style='text-align:center; color:#8892b0; font-size:0.8rem;'>"
        "⚠️ Predictions are estimates based on historical data. "
        "Consult a real estate professional before making decisions."
        "</p>",
        unsafe_allow_html=True
    )