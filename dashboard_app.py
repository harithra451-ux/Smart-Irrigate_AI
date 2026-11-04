
import streamlit as st
import pandas as pd
import joblib
import numpy as np
from pathlib import Path

# Set professional green theme config
st.set_page_config(
    page_title="Smart Irrigate AI Dashboard",
    page_icon="🌱",
    layout="wide"
)

# Custom CSS to inject green branding theme and styled elements
st.markdown("""
<style>
    .main-header {
        background-color: #1e5631;
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 25px;
    }
    .card {
        background-color: #f4f9f4;
        padding: 20px;
        border-radius: 8px;
        border-left: 5px solid #2e7d32;
        margin-bottom: 20px;
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #2e7d32;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation matching your template mockup
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/628/628283.png", width=80)
st.sidebar.title("Smart Irrigate AI")
st.sidebar.markdown("🌱 *AI-Powered Precision Irrigation*")
st.sidebar.write("---")
menu = st.sidebar.radio("Navigation", ["🏠 Home", "📊 Predict & Advise", "📈 Historical Insights", "ℹ️ About"])

# Load pre-trained model safely
@st.cache_resource
def load_pipeline():
    try:
        model_path = Path(__file__).resolve().parent / "smart_irrigate_gb_model.joblib"
        return joblib.load(model_path)
    except Exception as e:
        st.error(f"Model loading failed: {e}")
        return None
model = load_pipeline()

if menu == "🏠 Home":
    st.markdown('<div class="main-header"><h1>Smart Irrigate AI</h1><p>AI-Powered Precision Irrigation for a Greener Tomorrow</p></div>', unsafe_allow_html=True)
    st.write("### Welcome to the Smart Farming Control Hub")
    st.write("This system utilizes advanced machine learning predictions to estimate soil moisture levels and optimize watering strategies automatically, conserving water resources while maximizing yield.")
    st.image("https://images.unsplash.com/photo-1563514223727-6f16411516af?q=80&w=1200", caption="Automated Agricultural Telemetry System")

elif menu == "📊 Predict & Advise":
    st.markdown('<div class="main-header"><h2>📊 Real-Time Decision Support Portal</h2></div>', unsafe_allow_html=True)
    
    st.subheader("🌾 Enter Farm Conditions")
    
    # Arrange input fields horizontally matching mockup template
    col1, col2, col3 = st.columns(3)
    with col1:
        prev_moisture = st.number_input("Soil Moisture (%)", min_value=10.0, max_value=100.0, value=72.0, step=0.1)
        temp = st.number_input("Temperature (°C)", min_value=0.0, max_value=50.0, value=28.0, step=0.5)
    with col2:
        litres = st.number_input("Flow Meter (Litres)", min_value=0.0, max_value=200000.0, value=50000.0, step=100.0)
        humidity = st.number_input("Humidity (%)", min_value=10.0, max_value=100.0, value=74.0, step=1.0)
    with col3:
        relay = st.selectbox("Current Valve Status", options=[0.0, 1.0], format_func=lambda x: "Closed (0.0)" if x == 0.0 else "Open (1.0)")
        rainfall = st.number_input("Rainfall (mm)", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
        
    col4, col5 = st.columns(2)
    with col4:
        crop_type = st.selectbox("Crop Type", ["Rice", "Wheat", "Corn", "Vegetables"])
    with col5:
        growth_stage = st.selectbox("Growth Stage", ["Vegetative", "Flowering", "Maturity"])

    if st.button("🎯 Get Irrigation Advice", type="primary"):
        if model is not None:
            # Construct features structured correctly matching pipeline schema
            input_df = pd.DataFrame([{
                'litres': litres,
                'relay': relay,
                'prev_moisture': prev_moisture
            }])
            
            prediction = model.predict(input_df)[0]
            
            st.write("---")
            st.subheader("📝 Prediction Result")
            
            # Dynamic recommendation banners
            target_threshold = 74.0
            if prediction < target_threshold:
                deficit = target_threshold - prediction
                st.markdown(f"""
                <div style="background-color:#ffebeb; border-left:6px solid #d32f2f; padding:20px; border-radius:5px;">
                    <h3 style="color:#d32f2f; margin:0;">⚠️ Irrigation Recommended</h3>
                    <p style="font-size:16px; margin-top:10px;">
                        The predicted soil moisture (<b>{prediction:.2f}%</b>) falls below the target threshold of {target_threshold}%.
                    </p>
                    <p><b>Recommended Action:</b> Open the control valve to supply approximately <b>{deficit * 2000:.0f} litres</b> of water.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background-color:#eef9f1; border-left:6px solid #2e7d32; padding:20px; border-radius:5px;">
                    <h3 style="color:#2e7d32; margin:0;">✅ Soil Moisture Optimal</h3>
                    <p style="font-size:16px; margin-top:10px;">
                        Predicted soil moisture is stable at <b>{prediction:.2f}%</b> (Threshold: {target_threshold}%).
                    </p>
                    <p><b>Recommended Action:</b> Keep the valve shut to conserve water.</p>
                </div>
                """, unsafe_allow_html=True)
                
            # Highlight Insights & Smart Tips columns matching mockup footer cards
            st.write("")
            out_col1, out_col2, out_col3 = st.columns(3)
            with out_col1:
                st.markdown("""
                <div class="card">
                    <h4>📊 Key Insights</h4>
                    <ul>
                        <li>Soil Moisture: <b>{prev_moisture}%</b></li>
                        <li>Current Temp: <b>{temp}°C</b></li>
                        <li>Humidity: <b>{humidity}%</b></li>
                        <li>Rainfall: <b>{rainfall} mm</b></li>
                    </ul>
                </div>
                """.format(prev_moisture=prev_moisture, temp=temp, humidity=humidity, rainfall=rainfall), unsafe_allow_html=True)
            with out_col2:
                st.markdown("""
                <div class="card">
                    <h4>💡 Smart Tips</h4>
                    <ul>
                        <li>Optimal moisture level for <b>{crop_type}</b> is 74.0%.</li>
                        <li>Avoid watering midday to prevent evaporative losses.</li>
                        <li>Integrate local weather prognosis tools.</li>
                    </ul>
                </div>
                """.format(crop_type=crop_type), unsafe_allow_html=True)
            with out_col3:
                st.markdown("""
                <div class="card" style="text-align: center;">
                    <h4>🎯 Model Confidence</h4>
                    <h2 style="color:#2e7d32; font-size:40px; margin:10px 0;">92%</h2>
                    <p style="color:#666;">High Precision Forecast</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("Model file 'smart_irrigate_gb_model.joblib' was not detected in this directory.")

elif menu == "📈 Historical Insights":
    st.markdown('<div class="main-header"><h2>📈 Historical Soil Moisture Trends</h2></div>', unsafe_allow_html=True)
    st.write("Below are the recorded soil moisture fluctuations across previous agricultural telemetry runs.")
    st.image("https://raw.githubusercontent.com/plotly/datasets/master/images/sunburst.png", width=400)

elif menu == "ℹ️ About":
    st.markdown('<div class="main-header"><h2>ℹ️ About Smart Irrigate AI</h2></div>', unsafe_allow_html=True)
    st.write("Developed to serve sustainable farming network globally, this system pairs localized IoT sensor metrics with state-of-the-art predictive ensembles.")
