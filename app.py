import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Scam Sniffer AI",
    page_icon="🛡️",
    layout="centered"
)

# --- SIDEBAR FOR API KEY ---
with st.sidebar:
    st.header("🔑 Setup")
    api_key = st.text_input("Enter Google API Key:", type="password")
    st.markdown("[Get a Free Key Here](https://aistudio.google.com/app/apikey)")
    st.info("Your key is not saved. It's only used for this session.")

# --- MAIN UI ---
st.title("🛡️ Scam Sniffer AI")
st.markdown("""
**Upload a screenshot** of a suspicious email, SMS, or website. 
Our AI cybersecurity analyst will detect phishing indicators, fake urgency, and malicious patterns.
""")

# --- THE AI LOGIC ---
def analyze_scam(image_data, key):
    # Configure the API with the user's key
    genai.configure(api_key=key)
    
    # Use the fast and free-tier eligible model
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # The "Cybersecurity Expert" Prompt
    prompt = """
    You are a highly experienced Cybersecurity Analyst. Analyze this image for social engineering and phishing attacks.
    
    Output your analysis in this structured format:
    1. **VERDICT**: [SAFE / CAUTION / HIGH RISK]
    2. **RISK SCORE**: [0-100]/100
    3. **RED FLAGS**: List specific visual or textual indicators (e.g., 'Urgency: Act now', 'Mismatched URL', 'Generic Greeting').
    4. **EXPLANATION**: A brief summary of why this is suspicious or safe.
    5. **RECOMMENDATION**: What should the user do? (e.g., Delete, Block, Verify).
    
    Be concise and professional.
    """
    
    try:
        response = model.generate_content([prompt, image_data])
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# --- FILE UPLOADER ---
uploaded_file = st.file_uploader("Drop your screenshot here...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Display the image user uploaded
    image = Image.open(uploaded_file)
    st.image(image, caption="Your Screenshot", use_container_width=True)
    
    # The "Analyze" Button
    if st.button("🔍 Analyze Risk"):
        if not api_key:
            st.error("⚠️ Please enter your Google API Key in the sidebar first!")
        else:
            with st.spinner("Scanning for threats..."):
                result = analyze_scam(image, api_key)
                st.markdown("### 📝 Security Report")
                st.markdown("---")
                st.markdown(result)

# --- FOOTER ---
st.markdown("---")
st.caption("⚠️ Disclaimer: AI can make mistakes. Always verify sensitive information manually.")