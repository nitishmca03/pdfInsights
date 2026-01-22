
import zipfile
import os

# The specific files needed for the Python Streamlit app
# This intentionally excludes the old React/Node.js files
files_to_zip = [
    'streamlit_app.py',
    'requirements.txt',
    'README.md',
    '.gitignore',
    'metadata.json'
]

output_filename = 'pdf_insight_app.zip'

def create_zip():
    print(f"📦 Creating archive: {output_filename}...")
    
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files_to_zip:
            if os.path.exists(file):
                print(f"  + Adding {file}")
                zipf.write(file)
            else:
                print(f"  ⚠️ Warning: {file} not found in current directory")

    print(f"\n✅ Success! Created {output_filename}")
    print("   You can now upload this zip file to GitHub or share it.")

if __name__ == "__main__":
    create_zip()
