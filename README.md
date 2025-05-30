# Text Translator Streamlit App

A beautiful Streamlit web application for translating text using the Google Cloud Translation API (Free Tier). This app supports over 249 languages, with a default setup for translating English to Hindi, and is designed to handle texts like the 614-character sample about human migration to the Indian subcontinent. Results are displayed in a styled table and saved to a CSV file.

## Features
- **User-Friendly Interface**: Clean, blue-themed UI with a centered layout, custom CSS, and responsive design.
- **Language Support**: Translate text between 249+ languages, with auto-detection for the source language.
- **Input Flexibility**: Supports large texts (e.g., 614 characters) within the free tier’s 500,000-character/month limit.
- **Output**: Displays translations in a table, shows full translated text, and saves results to `translations.csv`.
- **Error Handling**: Robust checks for API issues, empty inputs, and invalid credentials.

## Prerequisites
- **Python 3.6+**: Ensure Python is installed (`python --version`).
- **Google Cloud Account**: Required for the Translation API free tier (500,000 characters/month).
- **Virtual Environment**: Recommended to manage dependencies.
- **JSON Key File**: A Google Cloud service account key for API authentication.

## Setup Instructions
1. **Clone or Download the Repository**:
   - Copy the files (`app.py`, `google_cloud.json`) to `e:/translate/` or clone the repository if hosted.
   - Ensure `google_cloud.json` is placed at `e:/translate/google_cloud.json`.

2. **Set Up Google Cloud**:
   - Create a Google Cloud project in the [Google Cloud Console](https://console.cloud.google.com).
   - Enable the **Cloud Translation API** under **APIs & Services** > **Library**.
   - Create a service account key under **APIs & Services** > **Credentials**:
     - Select **Create Credentials** > **Service Account**.
     - Assign the role **Cloud Translation API Editor**.
     - Download the JSON key and rename it to `google_cloud.json`.
     - Move it to `e:/translate/google_cloud.json`.
   - Enable billing for your project (required for free tier, no charges within 500,000 characters/month).

3. **Install Dependencies**:
   - Activate your virtual environment (if using one):
     ```bash
     cd e:/translate
     .\venv\Scripts\activate
     ```
   - Install required packages:
     ```bash
     pip install streamlit pandas google-cloud-translate
     ```

4. **Set Environment Variable**:
   - In the terminal (Windows), set the path to the JSON key:
     ```bash
     set GOOGLE_APPLICATION_CREDENTIALS=e:/translate/google_cloud.json
     ```

## Running the App
1. **Start the Streamlit App**:
   ```bash
   cd e:/translate
   streamlit run app.py