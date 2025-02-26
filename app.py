from urllib import response
import streamlit as st
import pint 
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Initialize Gemini AI
genai.configure(api_key=api_key)

# Initialize Pint for unit conversion
ureg = pint.UnitRegistry()

# Function to convert units (fixing temperature conversion issue)
def convert_units(value, from_unit, to_unit):
    try:
        if from_unit in ["celsius", "fahrenheit", "kelvin"] or to_unit in ["celsius", "fahrenheit", "kelvin"]:
            # Handle temperature conversions separately
            if from_unit == "celsius" and to_unit == "fahrenheit":
                result = (value * 9/5) + 32
            elif from_unit == "fahrenheit" and to_unit == "celsius":
                result = (value - 32) * 5/9
            elif from_unit == "celsius" and to_unit == "kelvin":
                result = value + 273.15
            elif from_unit == "kelvin" and to_unit == "celsius":
                result = value - 273.15
            elif from_unit == "fahrenheit" and to_unit == "kelvin":
                result = (value - 32) * 5/9 + 273.15
            elif from_unit == "kelvin" and to_unit == "fahrenheit":
                result = (value - 273.15) * 9/5 + 32
            else:
                return "Invalid temperature conversion"
            return f"{value} {from_unit} = {result:.2f} {to_unit}"
        else:
            # Normal unit conversions using Pint
            result = (value * ureg(from_unit)).to(to_unit)
            return f"{value} {from_unit} = {result}"    
    except pint.DimensionalityError:
        return "Invalid conversion"

# AI function using Gemini
def ask_gemini(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text if response else "Error fetching"

# Streamlit UI
st.set_page_config(page_title="Unit Converter & AI Assistant", layout="wide")

# Apply CSS Styling
st.markdown("""
    <style>
    /* General Styling */
    body {
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #41644A !important;
        color: white !important;
        font-size: 16px !important;
        padding: 10px 24px !important;
        border-radius: 8px !important;
        border: none !important;
        transition: background-color 0.3s ease, transform 0.2s ease !important;
    }
    .stButton>button:hover {
        background-color: #5D8736 !important;
        transform: scale(1.05) !important;
    }
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        border: 2px solid #4CAF50 !important;
        border-radius: 10px !important;
        padding: 10px !important;
        transition: border-color 0.3s ease !important;
        height: 50px !important;  /* Adjust height */
         
        
    }
    .stTextInput>div>div>input:focus, .stSelectbox>div>div>div:focus {
        border-color: #41644A !important;
            
    }
    
    .stMarkdown h1 {
        color: #4CAF50 !important;
        text-align: center !important;
        animation: fadeIn 2s !important;
    }
    .stMarkdown h2, .stMarkdown h3 {
        color: #4CAF50 !important;
    }
    .stSuccess {
        background-color: #d4edda !important;
        color: #155724 !important;
        padding: 10px !important;
        border-radius: 8px !important;
        border: 1px solid #c3e6cb !important;
        animation: slideIn 0.5s ease !important;
    }
    .stError {
        background-color: #123524 !important;
        color: #721c24 !important;
        padding: 10px !important;
        border-radius: 8px !important;
        border: 1px solid #f5c6cb !important;
        animation: shake 0.5s !important;
    }
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes slideIn {
        from { transform: translateY(-20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    @keyframes shake {
        0% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        50% { transform: translateX(10px); }
        75% { transform: translateX(-10px); }
        100% { transform: translateX(0); }
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌍 Ultimate Unit Converter")
st.markdown("Convert any unit to another in real-time! Supports length, mass, temperature, volume, speed, and more.")

# Define supported units
unit_categories = {
    "Length": ["meter", "foot", "inch", "mile", "kilometer", "light_year"],
    "Mass": ["kilogram", "gram", "pound", "ounce", "ton"],
    "Temperature": ["celsius", "fahrenheit", "kelvin"],
    "Volume": ["liter", "gallon", "cubic_meter", "cubic_inch"],
    "Speed": ["meter_per_second", "kilometer_per_hour", "mile_per_hour"],
    "Energy": ["joule", "calorie", "electron_volt"],
}

# Input fields
st.subheader("Enter Your Conversion")

col1, col2, col3 = st.columns(3)

with col1:
    value = st.number_input("Enter value:", value=1.0, step=0.1)

with col2:
    category = st.selectbox("Select unit category:", list(unit_categories.keys()))

with col3:
    from_unit = st.selectbox("Select from unit:", unit_categories[category])

# Target unit
target_unit = st.selectbox("Select target unit:", unit_categories[category])

# Convert button
if st.button("Convert"):
    with st.spinner("Converting..."):  # Add a loading spinner
        result = convert_units(value, from_unit, target_unit)
        if "Invalid" not in result:
            st.success(f"✅ {result}")
        else:
            st.error("❌ Invalid conversion. Please check your units.")

# AI Assistant
st.subheader("💬 Ask AI (Powered by Gemini)")
user_query = st.text_area("Enter your question:")

if st.button("Ask AI"):
    if user_query:
        ai_response = ask_gemini(user_query)
        st.info(f"🤖 AI Response: {ai_response}")
    else:
        st.warning("⚠️ Please enter a question.")

# Footer
st.markdown("---")
st.markdown("👩‍💻 Developed by **Anousha Baig** | 🚀 Powered by **Google Gemini AI & Streamlit**")
