
# PDF Insight AI (Python)

A Streamlit application that uses Google Gemini 3 Flash and PyPDF to summarize and answer questions about PDF documents.

## Prerequisites

- Python 3.9+
- A Google Cloud Project with the Gemini API enabled.

## Local Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set your API Key**:
   Create a file named `.env` (optional) or export it in your terminal:
   ```bash
   export API_KEY="your_gemini_api_key_here"
   ```

3. **Run the app**:
   ```bash
   streamlit run streamlit_app.py
   ```

## Deployment Guide

### Option 1: Streamlit Community Cloud (Recommended)
This is the easiest way to deploy Streamlit apps for free and works perfectly with GitHub.

1. **Push to GitHub**:
   Initialize a repository and push this code (see "How to Push to GitHub" below).
2. Go to [share.streamlit.io](https://share.streamlit.io/).
3. Click **"New app"**.
4. Select your GitHub repository and the branch.
5. Set `Main file path` to `streamlit_app.py`.
6. Click **"Advanced settings"** and add your `API_KEY` in the "Secrets" section.
   ```toml
   API_KEY = "your_key_here"
   ```
7. Click **Deploy**.

## How to Push to GitHub

**Note:** The `.gitignore` file has been configured to ignore the old React files (`.tsx`, `components/`, etc.) so your repository remains clean.

1. **Initialize Git**:
   ```bash
   git init
   ```

2. **Add files**:
   ```bash
   git add .
   ```

3. **Commit changes**:
   ```bash
   git commit -m "Initial commit: PDF Insight AI with Gemini"
   ```

4. **Connect to GitHub**:
   *Create a new empty repository on GitHub first.*
   ```bash
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

## Download the Code

There are two ways to download the code as a zip file:

1. **Via the App**: Run the app and click the **"Download Source Code"** button in the sidebar.
2. **Via Script**: Run the helper script in your terminal:
   ```bash
   python create_zip.py
   ```
