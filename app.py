from flask import Flask, render_template, request, send_file
import os
from utils import ocr, compare_sentences, create_pdf

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file1 = request.files['file1']
        file2 = request.files['file2']

        if not file1 or not file2:
            return "Please upload both PDF files."

        # Extract text from the uploaded PDF files
        text_org = ocr(file1)
        text_mod = ocr(file2)

        # Compare the extracted texts
        results = compare_sentences(text_org, text_mod)
        
        # Generate a PDF with the comparison results
        pdf_filename = 'result.pdf'
        create_pdf(results, pdf_filename)
        
        # Send the generated PDF as a downloadable file
        return send_file(pdf_filename, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
