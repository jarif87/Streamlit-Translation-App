import streamlit as st
from google.cloud import translate_v2 as translate
import pandas as pd
import os

# Set page configuration for a professional look
st.set_page_config(
    page_title="Text Translator - Google Cloud",
    page_icon="🌐",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
    }
    .title {
        font-family: 'Arial', sans-serif;
        color: #1f77b4;
        text-align: center;
        font-size: 2.5em;
        margin-bottom: 0.5em;
    }
    .subtitle {
        font-family: 'Arial', sans-serif;
        color: #555555;
        text-align: center;
        font-size: 1.2em;
        margin-bottom: 2em;
    }
    .stButton>button {
        background-color: #1f77b4;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 1em;
    }
    .stTextArea textarea {
        border: 2px solid #1f77b4;
        border-radius: 5px;
        font-size: 1em;
    }
    .stSelectbox select {
        border: 2px solid #1f77b4;
        border-radius: 5px;
    }
    .result-box {
        background-color: white;
        padding: 15px;
        border-radius: 5px;
        border: 1px solid #ddd;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Google Cloud Translation client
try:
    # Replace with your JSON key path
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_cloud.json"
    client = translate.Client()
except Exception as e:
    st.error(f"Failed to initialize Google Cloud Translation client: {str(e)}. Please check your JSON key file and environment variable.")
    st.stop()

# Function to get supported languages
@st.cache_data
def get_supported_languages():
    try:
        languages = client.get_languages()
        return {lang["name"]: lang["language"] for lang in languages}
    except Exception as e:
        st.error(f"Failed to fetch supported languages: {str(e)}")
        return {}

# Function to translate text
def translate_text(text, source_lang, target_lang):
    try:
        if not text.strip():
            return "Error: Input text is empty", None
        result = client.translate(
            text,
            source_language=source_lang if source_lang != "auto" else None,
            target_language=target_lang
        )
        return result["translatedText"], result.get("detectedSourceLanguage", source_lang)
    except Exception as e:
        return f"Error: {str(e)}", None

# Streamlit app layout
st.markdown('<div class="title">Text Translator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Translate text using Google Cloud Translation API (Free Tier)</div>', unsafe_allow_html=True)

# Sidebar for language selection
with st.sidebar:
    st.header("Translation Settings")
    languages = get_supported_languages()
    if not languages:
        st.error("No languages available. Please check your API setup.")
        st.stop()
    source_lang_name = st.selectbox("Source Language", ["Auto-detect"] + list(languages.keys()), index=0)
    target_lang_name = st.selectbox("Target Language", list(languages.keys()), index=list(languages.keys()).index("Hindi") if "Hindi" in languages else 0)
    source_lang = "auto" if source_lang_name == "Auto-detect" else languages[source_lang_name]
    target_lang = languages[target_lang_name]

# Input text area with your sample text
default_text = """According to consensus in modern genetics anatomically modern humans first arrived on the Indian subcontinent from Africa between 73,000 and 55,000 years ago.[1] However, the earliest known human remains in South Asia date to 30,000 years ago. Settled life, which involves the transition from foraging to farming and pastoralism, began in South Asia around 7,000 BCE. At the site of Mehrgarh presence can be documented of the domestication of wheat and barley, rapidly followed by that of goats, sheep, and cattle.[2] By 4,500 BCE, settled life had spread more widely,[2] and began to gradually evolve into the Indus Valley Civilization, an early civilization of the Old world, which was contemporaneous with Ancient Egypt and Mesopotamia. This civilisation flourished between 2,500 BCE and 1900 BCE in what today is Pakistan and north-western India, and was noted for its urban planning, baked brick houses, elaborate drainage, and water supply.[3]"""
input_text = st.text_area("Enter text to translate", value=default_text, height=200)

# Translate button
if st.button("Translate"):
    with st.spinner("Translating..."):
        translated_text, detected_source_lang = translate_text(input_text, source_lang, target_lang)
        if "Error" in translated_text:
            st.error(translated_text)
        else:
            # Display results
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.subheader("Translation Results")
            results = [{
                "Original Text": input_text[:100] + "..." if len(input_text) > 100 else input_text,
                "Source Language": [name for name, code in languages.items() if code == detected_source_lang][0] if detected_source_lang != "auto" else "Auto-detected",
                "Target Language": target_lang_name,
                "Translated Text": translated_text
            }]
            df = pd.DataFrame(results)
            st.dataframe(df, use_container_width=True)
            st.markdown(f"**Full Translated Text:**:\n\n{translated_text}")
            st.markdown('</div>', unsafe_allow_html=True)

            # Save to CSV
            df.to_csv("translations.csv", index=False)
            st.success("Translations saved to translations.csv")

# Footer
st.markdown('<div class="subtitle">Powered by Google Cloud Translation API | Free Tier (500,000 characters/month)</div>', unsafe_allow_html=True)