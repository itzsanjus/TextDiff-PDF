from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import os
from utils import convert_pdf_to_images, compare_sentences, create_pdf, compare_pdfs, length_match, extract_text_with_pytesseract

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file1 = request.files['file1']
        file2 = request.files['file2']
        compute_hash = 'compute_hash' in request.form  # Check if the checkbox is selected

        if not file1 or not file2:
            flash("Please upload both PDF files.")
            return redirect(url_for('index'))


        if compare_pdfs(file1,file2):
            flash("The uploaded PDFs are identical.")
            return redirect(url_for('index'))

        pdf_list1 = convert_pdf_to_images(file1)
        pdf_list2 = convert_pdf_to_images(file2)
        
        
        # Extract text from the uploaded PDF files
        text_org = extract_text_with_pytesseract(pdf_list1)
        text_mod = extract_text_with_pytesseract(pdf_list2)

        if not length_match(text_org, text_mod):
            flash("The uploaded PDFs are completely different.")
            return redirect(url_for('index'))

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

