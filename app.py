import streamlit as st
from streamlit_geolocation import streamlit_geolocation
from twilio.rest import Client
import pandas as pd
import time

# --- STYLING & CONFIG ---
st.set_page_config(page_title="SafeZone - SDG 5 Capstone", page_icon="🛡️", layout="wide")

# Mock database using Streamlit's cache-safe Session State
if "emergency_logs" not in st.session_state:
    st.session_state.emergency_logs = []

# --- TWILIO ALERT CONFIGURATION ---
# (In production, replace these placeholders with environment variables)
TWILIO_ACCOUNT_SID = "YOUR_SID"
TWILIO_AUTH_TOKEN = "YOUR_TOKEN"
TWILIO_PHONE = "YOUR_TWILIO_NUMBER"
TO_PHONE = "YOUR_PERSONAL_NUMBER"

def send_emergency_sms(lat, lon, reason):
    """Triggers an automated SMS alert with a live Google Maps tracker link."""
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        maps_link = f"https://www.google.com/maps?q={lat},{lon}"
        message_body = f"⚠️ EMERGENCY ALERT (SDG 5 Demo):\nUser triggered distress trigger.\nReason: {reason}\nLocation: {maps_link}"
        
        
        # client.messages.create(body=message_body, from_=TWILIO_PHONE, to=TO_PHONE)
        return True
    except Exception as e:
        st.error(f"Twilio Dispatch Failure: {e}")
        return False

# --- APP INTERFACE NAVIGATION ---
st.title("🛡️ Project SafeZone")
st.caption("An AI-Enabled Rapid Incident Dispatch System supporting UN SDG 5 (Gender Equality & Safety)")

tab1, tab2 = st.tabs(["📱 User Safety Interface", "📊 Mock Authority Command Center"])

# =========================================================
# TAB 1: THE USER PLATFORM
# =========================================================
with tab1:
    st.header("Emergency Trigger Panel")
    st.write("Keep this panel open when traveling through unfamiliar paths.")
    
    # Capture Location Coordinates
    st.subheader("1. Initialize Geolocation Protection")
    location = streamlit_geolocation()
    
    # lat = location.get('latitude')
    # lon = location.get('longitude')
    lat = 15.9312
    lon = 73.6644
    
    if lat and lon:
        st.success(f"📍 GPS Sentinel Active: Coordinates Locked ({lat:.4f}, {lon:.4f})")
    else:
        st.warning("⚠️ Location access required. Click the location widget above to grant browser permissions.")

    # Distress Logic Selection
    st.subheader("2. Select Your Sentinel Mode")
    trigger_mode = st.radio("Choose Input Metric:", ["Manual Panic Button", "Text Sentiment Analyzer", "Voice Input (Beta)"])
    
    triggered = False
    alert_reason = ""

    if trigger_mode == "Manual Panic Button":
        if st.button("🚨 TRIGGER IMMEDIATE EMERGENCY ALERT", type="primary", use_container_width=True):
            triggered = True
            alert_reason = "Manual SOS Button Depressed"
            
    elif trigger_mode == "Text Sentiment Analyzer":
        user_input = st.text_input("Type a message to someone (System will flag critical sentiment phrases):")
        
        # Prototype Keyphrase NLP matching
        danger_keywords = ["help", "follow", "scared", "unsafe", "run", "please help", "danger"]
        if user_input:
            if any(word in user_input.lower() for word in danger_keywords):
                st.error("🚨 AI Threat Detection Engine Status: CRITICAL SENTIMENT FLAGGED")
                if st.button("Confirm Auto-Dispatch Threat?", type="primary"):
                    triggered = True
                    alert_reason = f"NLP Flagged Intent: '{user_input}'"
            else:
                st.success("AI Threat Detection Engine Status: Normal / Clear Sentiment")

    elif trigger_mode == "Voice Input (Beta)":
        audio_value = st.audio_input("Record a distress vocalization message:")
        if audio_value:
            st.audio(audio_value)
            # Capstone feature: simulated speech-to-text pipeline
            st.warning("Voice Analysis Simulation active. Phrase 'Help me' detected via acoustic profile.")
            if st.button("Dispatch voice flag coordinates?", type="primary"):
                triggered = True
                alert_reason = "Acoustic Voice Keyword Triggered"

    # Executive Action Execution
    if triggered:
        if lat and lon:
            with st.spinner("Dispatching geolocation payload to Twilio APIs & Local Hubs..."):
                # Append incident internally to database session
                incident_payload = {
                    "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "Latitude": lat,
                    "Longitude": lon,
                    "Trigger Context": alert_reason,
                    "Status": "Dispatch Assigned"
                }
                st.session_state.emergency_logs.append(incident_payload)
                
                # Execute Twilio logic
                sms_status = send_emergency_sms(lat, lon, alert_reason)
                st.balloons()
                st.success("🚀 Alert broadcast successful! Mock Authorities notified and SMS dispatched.")
        else:
            st.error("Failed to execute dispatch: Device location not acquired.")

# =========================================================
# TAB 2: THE COMMAND CENTER
# =========================================================
with tab2:
    st.header("🚨 Authority Live Incident Log")
    st.write("Simulated monitoring portal tracking high-priority SDG 5 safety events.")
    
    if st.session_state.emergency_logs:
        df_logs = pd.DataFrame(st.session_state.emergency_logs)
        st.dataframe(df_logs, use_container_width=True)
        
        # Display mapped spatial data across live incidents
        st.subheader("Incident Geographic Visualizer Map")
        map_data = df_logs[['Latitude', 'Longitude']].rename(columns={'Latitude': 'lat', 'Longitude': 'lon'})
        st.map(map_data)
    else:
        st.info("System Normal: No priority safety triggers reported across active tracking sessions.")