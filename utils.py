import hashlib
import pypdfium2 as pdfium
from io import BytesIO
from PIL import Image
from pytesseract import image_to_string
import re
import difflib
from nltk import sent_tokenize

def compute_pdf_hash(pdf_file):
    pdf_bytes = pdf_file.read()

    hash_object = hashlib.sha256(pdf_bytes)

    return hash_object.hexdigest()

def compare_pdfs(pdf_file1, pdf_file2) -> bool:
    # Compute hashes for both PDF files
    hash1 = compute_pdf_hash(pdf_file1)
    hash2 = compute_pdf_hash(pdf_file2)

    return hash1 == hash2



def convert_pdf_to_images(file_path, scale=300/72):

    pdf_file = pdfium.PdfDocument(file_path)
    page_indices = [i for i in range(len(pdf_file))]

    renderer = pdf_file.render(
        pdfium.PdfBitmap.to_pil,
        page_indices = page_indices,
        scale = scale,
    )

    list_final_images = []

    for i, image in zip(page_indices, renderer):

        image_byte_array = BytesIO()
        image.save(image_byte_array, format='jpeg', optimize=True)
        image_byte_array = image_byte_array.getvalue()
        list_final_images.append(dict({i:image_byte_array}))

    return list_final_images

def length_match(text1, text2, tolerance=0.2):

    len1 = len(text1)
    len2 = len(text2)
    
    # Handle cases where one or both texts might be empty
    if len1 == 0 or len2 == 0:
        return False
    
    # Calculate the ratio of the lengths
    length_ratio = min(len1, len2) / max(len1, len2)
    
    # Return True if the ratio is within the tolerance, else False
    return length_ratio >= (1 - tolerance)

def extract_text_with_pytesseract(list_dict_final_images):

    image_list = [list(data.values())[0] for data in list_dict_final_images]
    image_content = []

    for index, image_bytes in enumerate(image_list):

        image = Image.open(BytesIO(image_bytes))
        raw_text = str(image_to_string(image))
        image_content.append(raw_text)

    return "\n".join(image_content)

def split_into_sentences(text):
     # Define a regex pattern to match the tokens you want to remove
    pattern = r'(?<!\S)(\d+(\.\d+)*\.\s*|I[VX]?[I]{0,3}\.\s*)'
    # Remove the tokens from the text
    text = re.sub(pattern, '', text)
    # Strip the text and remove all extra white spaces
    cleaned_text = ' '.join(text.split())
    
    # Tokenize the cleaned text into sentences
    sentences = sent_tokenize(cleaned_text)
    return sentences

def compare_sentences(text1, text2, lower_threshold=0.5, upper_threshold=0.99):
    """
    Compares sentences from two texts and returns a list of results indicating whether they match,
    are modified, added, or deleted.
    Uses similarity thresholds to determine matches and modifications.
    """
    sentences1 = split_into_sentences(text1)
    sentences2 = split_into_sentences(text2)

    results = []
    matched_indices1 = set()
    matched_indices2 = set()

    # Compare each sentence in text2 against all sentences in text1
    for idx2, sent2 in enumerate(sentences2):
        best_match = None
        best_similarity = 0.0
        best_idx1 = None

        for idx1, sent1 in enumerate(sentences1):
            if idx1 in matched_indices1:
                continue

            similarity = difflib.SequenceMatcher(None, sent1, sent2).ratio()

            if similarity > best_similarity:
                best_similarity = similarity
                best_match = (idx2, "Match" if similarity >= upper_threshold else "Modified", similarity, sent1, sent2)
                best_idx1 = idx1

        if best_similarity >= lower_threshold:
            results.append(best_match)
            matched_indices1.add(best_idx1)
            matched_indices2.add(idx2)
        else:
            results.append((idx2, "Added", 0.0, None, sent2))
            matched_indices2.add(idx2)

    # Check for any sentences in text1 not found in text2
    for idx1, sent1 in enumerate(sentences1):
        if idx1 not in matched_indices1:
            results.append((None, "Deleted", 0.0, sent1, None))

    return results


from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

def create_pdf(results, filename="comparison_report.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    for index, result, similarity, para1, para2 in results:
        if result in ["Modified", "Deleted", "Added"]:
            if result == "Modified":
                story.append(Paragraph(f"<b>Sentence {index + 1 if index is not None else 'N/A'}: {result} (Similarity: {similarity:.2f})</b>", styles["Normal"]))
                story.append(Paragraph(f"<b>Original:</b> {para1}", styles["Normal"]))
                story.append(Paragraph(f"<b>Modified:</b> {para2}", styles["Normal"]))
            elif result == "Deleted":
                story.append(Paragraph(f"<b>Sentence {index + 1 if index is not None else 'N/A'}: {result}</b>", styles["Normal"]))
                story.append(Paragraph(f"<b>Original:</b> {para1}", styles["Normal"]))
            elif result == "Added":
                story.append(Paragraph(f"<b>Sentence {index + 1 if index is not None else 'N/A'}: {result}</b>", styles["Normal"]))
                story.append(Paragraph(f"<b>Modified:</b> {para2}", styles["Normal"]))
            story.append(Spacer(1, 12))
            story.append(Spacer(1, 12))

    doc.build(story)
