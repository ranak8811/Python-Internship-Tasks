import streamlit as st
import requests

st.set_page_config(page_title="Samsung Advisor", page_icon="📱")

st.title("📱 Samsung Phone Advisor")
st.write("Click on a question below to get an answer from the AI agent.")

API_URL = "http://127.0.0.1:8000/ask"

# list of sample questions
questions = [
    "Tell me about Samsung Galaxy F17",
    "What are the specs of Samsung Galaxy S25 FE?",
    "Compare Galaxy S25 FE and Z Fold7 for photography.",
    "Which Samsung phone has the best battery under $1000?",
    "Show me the specs of Galaxy Z Fold7",
    "Tell me about today's weather"
]

if 'response' not in st.session_state:
    st.session_state['response'] = None

st.subheader("💡 Example Questions")

for q in questions:
    if st.button(q):
        with st.spinner("Consulting the agent..."):
            try:
                # sending request to the backend
                resp = requests.post(API_URL, json={"question": q})
                
                if resp.status_code == 200:
                    data = resp.json()
                    st.session_state['response'] = data.get("answer", "No answer received.")
                else:
                    st.session_state['response'] = f"Error: {resp.status_code} - {resp.text}"
            except requests.exceptions.ConnectionError:
                st.session_state['response'] = "Error: Could not connect to the backend. Is 'uvicorn' running?"

st.markdown("---")

if st.session_state['response']:
    st.success("Analysis Result:")
    st.markdown(st.session_state['response'])
