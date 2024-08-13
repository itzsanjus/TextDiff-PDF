# PDF Comparison Tool

## Overview

The PDF Comparison Tool is a web application that allows users to upload two PDF files (an original and a modified), compares the text content from both files, and generates a PDF report with the comparison results. The tool highlights differences, modifications, additions, and deletions between the two documents.

## Features

- **Upload PDF Files:** Upload two PDF files for comparison.
- **Text Extraction:** Automatically extracts text from the uploaded PDF files.
- **Text Comparison:** Compares the text content and identifies differences.
- **Result PDF:** Generates a downloadable PDF report with the comparison results.

## Getting Started

### Prerequisites

- `Python 3.x`
- `Flask`
- `pytesseract`

### Installation

1. **Clone the Repository:**

   ```bash
   git clone <repository_url>
   cd <repository_directory>
2. **Install Python Dependencies:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

NLTK 'punkt' should also be present in the environment. So, the following code should run before starting the application in the same environment.
   ```bash
   import nltk
   nltk.download('punkt')
```
3. **Install Tesseract-OCR:**

   ```bash
   sudo apt-get install tesseract-ocr
   
4. **Prepare the Application:**

   Ensure that the utils.py file with the necessary utility functions is in the same directory as app.py.

5. **Run the Application:**

   ```bash
   python app.py
6. **Access the Application:**

   Open your web browser and navigate to http://127.0.0.1:5000/
   

## Usage
**Upload PDFs:**

Use the form to upload the two PDF files you want to compare.
Click "Compare and Download PDF" to submit the form.
Download Results:

After processing, a PDF report with the comparison results will be available for download.

## Contact
For any inquiries or feedback, please contact:

Developer: Sanju Sarkar
Email: sanjusarkar44@hotmail.com
