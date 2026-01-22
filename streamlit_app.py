
import streamlit as st
from google import genai
from google.genai import types
import pypdf
import os
import zipfile
import io

# -----------------------------------------------------------------------------
# Configuration & Setup
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="PDF Insight AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a cleaner look
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
    }
    div[data-testid="stChatMessage"] {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    div[data-testid="stChatMessage"].st-emotion-cache-1c7y2kd {
        background-color: #f3f4f6;
    }
    h1 {
        color: #4F46E5;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------

def create_zip_buffer():
    """Creates a zip file of the source code in memory."""
    buffer = io.BytesIO()
    files_to_zip = [
        'streamlit_app.py',
        'requirements.txt',
        'README.md',
        '.gitignore',
        'metadata.json',
        'create_zip.py'
    ]
    
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files_to_zip:
            if os.path.exists(file):
                zipf.write(file)
            else:
                # If running in some environments, files might not be strictly local, 
                # but for standard deployment this works.
                pass
                
    buffer.seek(0)
    return buffer

# -----------------------------------------------------------------------------
# Service Logic
# -----------------------------------------------------------------------------

def get_ai_client():
    api_key = os.environ.get("API_KEY")
    if not api_key:
        st.error("⚠️ API_KEY environment variable is missing.")
        st.stop()
    return genai.Client(api_key=api_key)

def extract_text_from_pdf(file):
    """Extracts text from a PDF file object using pypdf."""
    try:
        reader = pypdf.PdfReader(file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        st.error(f"Failed to extract text from PDF: {e}")
        return None

def generate_summary(client, text):
    """Generates a summary using Gemini."""
    prompt = f"""
    You are an expert document analyst. 
    Please provide a concise but comprehensive summary (gist) of the following document text.
    Focus on the main arguments, key findings, and important dates or figures if applicable.
    Format the output in clean Markdown using bullet points where appropriate.
    
    Document Text:
    {text[:500000]} 
    """
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error generating summary: {e}"

def generate_answer(client, doc_text, chat_history, question):
    """Generates an answer based on document context."""
    
    # Construct prompt with context
    prompt = f"""
    Context from the document:
    {doc_text[:500000]}

    Question: {question}
    
    Answer the question strictly based on the provided document context. 
    If the answer is not in the document, say so politely.
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="You are a helpful assistant answering questions about a provided PDF document."
            )
        )
        return response.text
    except Exception as e:
        return f"Error generating answer: {e}"

# -----------------------------------------------------------------------------
# UI Layout
# -----------------------------------------------------------------------------

def main():
    client = get_ai_client()

    # Sidebar for Upload & Utils
    with st.sidebar:
        st.title("📄 PDF Insight")
        st.write("Upload a document to get started.")
        
        uploaded_file = st.file_uploader("Upload PDF", type="pdf")
        
        if st.button("Clear / Reset", type="secondary"):
            st.session_state.clear()
            st.rerun()

        st.markdown("---")
        st.caption("Developer Tools")
        
        # Download Source Code Button
        zip_buffer = create_zip_buffer()
        st.download_button(
            label="📥 Download Source Code",
            data=zip_buffer,
            file_name="pdf_insight_app.zip",
            mime="application/zip",
            help="Download the full Python source code for this application."
        )

    # Main State Management
    if "pdf_text" not in st.session_state:
        st.session_state.pdf_text = None
    if "summary" not in st.session_state:
        st.session_state.summary = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "current_file" not in st.session_state:
        st.session_state.current_file = None

    # Processing Logic
    if uploaded_file:
        # Check if it's a new file
        if st.session_state.current_file != uploaded_file.name:
            with st.spinner("Processing PDF..."):
                text = extract_text_from_pdf(uploaded_file)
                if text:
                    st.session_state.pdf_text = text
                    st.session_state.current_file = uploaded_file.name
                    st.session_state.messages = [] # Reset chat
                    
                    with st.spinner("Generating summary..."):
                        summary = generate_summary(client, text)
                        st.session_state.summary = summary
                        
                        # Initial bot message
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": f"I've analyzed **{uploaded_file.name}**. You can read the summary on the left or ask me questions on the right!"
                        })

    # Main Content Area
    if st.session_state.pdf_text:
        col1, col2 = st.columns([1, 1], gap="large")

        # Left Column: Summary
        with col1:
            st.subheader("📝 Document Summary")
            st.markdown("---")
            st.markdown(st.session_state.summary)

        # Right Column: Chat
        with col2:
            st.subheader("💬 Q&A Chat")
            st.markdown("---")
            
            # Message Container
            chat_container = st.container(height=500)
            
            with chat_container:
                for msg in st.session_state.messages:
                    with st.chat_message(msg["role"]):
                        st.markdown(msg["content"])

            # Chat Input
            if prompt := st.chat_input("Ask a question about the PDF..."):
                # Append user message
                st.session_state.messages.append({"role": "user", "content": prompt})
                with chat_container:
                    with st.chat_message("user"):
                        st.markdown(prompt)
                    
                    # Generate and stream/show response
                    with st.chat_message("assistant"):
                        with st.spinner("Thinking..."):
                            response_text = generate_answer(
                                client,
                                st.session_state.pdf_text,
                                st.session_state.messages,
                                prompt
                            )
                            st.markdown(response_text)
                
                # Append assistant message
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                # Force rerun to update state properly if needed, usually streamlit handles this via the run loop
                
    else:
        # Empty State
        st.info("👈 Please upload a PDF file from the sidebar to begin.")
        st.markdown("""
        ### How it works
        1. **Upload**: Drag and drop your PDF file.
        2. **Analyze**: We extract the text and Gemini generates a summary.
        3. **Chat**: Ask specific questions about the document content.
        
        ### Get the Code
        You can download the full source code for this app by clicking the **Download Source Code** button in the sidebar.
        """)

if __name__ == "__main__":
    main()
