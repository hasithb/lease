import concurrent.futures
import re
from concurrent.futures import ThreadPoolExecutor
import joblib
from PyPDF2 import PdfFileReader
from flask import flash
from transformers import pipeline

# Load pre-trained model and vectorizer
model = joblib.load('lease_clause_classifier.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Ensure that vectorizer and model are defined
# from your_model_package import vectorizer, model

def process_text_file(file_path):
    try:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text_data = file.read()
        except UnicodeDecodeError:
            # Handle other encodings like 'ISO-8859-1', 'latin1', etc.
            with open(file_path, 'r', encoding='ISO-8859-1') as file:
                text_data = file.read()

        # Extract Information
        rent_clause_pattern = re.compile(r'Rent Clause: (.+)')
        rent_clause = re.search(rent_clause_pattern, text_data)
        extracted_data = {
            'Rent Clause': rent_clause.group(1) if rent_clause else 'Not found'
        }

        # Assume that you have functions or logic to extract clauses and sentences
        # these should be implemented based on your specific use-case and data
        clauses = extract_clauses(text_data)  # Implement this function based on your use case
        sentences = extract_sentences(text_data)  # Implement this function based on your use case

        # Apply ML Model
        vectorized_data = vectorizer.transform([text_data])
        prediction = model.predict(vectorized_data)
        print("Type of prediction: {type(prediction)}, prediction: {prediction}")  # Add this line

        # Now, ensure that prediction is indexable before proceeding.
        if isinstance(prediction, (list, tuple)) and prediction:
            extracted_data['Predicted Category'] = 'Key Term' if prediction[0] == 1 else 'Problem Clause'
        else:
            print("Unexpected prediction format: {prediction}")
            extracted_data['Predicted Category'] = 'Unknown'

        # Interpret Prediction
        extracted_data['Predicted Category'] = 'Key Term' if prediction[0] == 1 else 'Problem Clause'

        return clauses, sentences, extracted_data
    except Exception as e:
        print("Error processing text: {str(e)}")
        return None, None, {'error': str(e)}


# Placeholder for clause extraction logic, you need to define actual logic based on your needs
def extract_clauses(text):
    # Actual logic to extract clauses
    clauses = "Your clause extraction logic here"
    return clauses


# Placeholder for sentence extraction logic, you need to define actual logic based on your needs
def extract_sentences(text):
    # Actual logic to extract sentences
    sentences = "Your sentence extraction logic here"
    return sentences


# Remove or relocate the Celery task if it’s not utilized or create it as per the actual use-case requirements.
# Function to extract text from a PDF file
def process_uploaded_pdf(file):
    try:
        pdf_reader = PdfFileReader(file)
        lease_text_dict = {"Page {i}": page.extract_text() for i, page in enumerate(pdf_reader.pages, start=1)}
        return lease_text_dict
    except Exception as e:
        flash("Error processing PDF: {str(e)}")
        return None


# Function to get the summarizer pipeline
def get_summarizer():
    return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")


# Function to summarize text using the summarizer pipeline
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")


def summarize(text_dict):
    summarizer = get_summarizer()
    summarized_dict = {}
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(summarizer, text, {"max_length": 150, "min_length": 40, "do_sample": False}): page
                   for page, text in text_dict.items()}
        for future in concurrent.futures.as_completed(futures):
            page = futures[future]
            try:
                summarized_dict[page] = future.result()[0]['summary_text']
            except Exception as e:
                print(f"Error summarizing page {page}: {str(e)}")
    return summarized_dict


# Function to extract key clauses from the lease text
def extract_key_clauses(lease_text):
    # Define regular expressions for key clauses (you can add more)
    rent_clause_pattern = re.compile(r'Rent Clause: (.+)')
    deposit_clause_pattern = re.compile(r'Deposit Clause: (.+)')
    termination_clause_pattern = re.compile(r'Termination Clause: (.+)')
    maintenance_clause_pattern = re.compile(r'Maintenance Clause: (.+)')

    # Extract key clauses using regex
    rent_clause = re.search(rent_clause_pattern, lease_text)
    deposit_clause = re.search(deposit_clause_pattern, lease_text)
    termination_clause = re.search(termination_clause_pattern, lease_text)
    maintenance_clause = re.search(maintenance_clause_pattern, lease_text)

    # Create a dictionary to store the extracted clauses
    extracted_clauses = {
        'Rent Clause': rent_clause.group(1) if rent_clause else 'Not found',
        'Deposit Clause': deposit_clause.group(1) if deposit_clause else 'Not found',
        'Termination Clause': termination_clause.group(1) if termination_clause else 'Not found',
        'Maintenance Clause': maintenance_clause.group(1) if maintenance_clause else 'Not found',
    }

    return extracted_clauses


def process_your_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='ISO-8859-1') as file:
                content = file.read()
            return content
        except Exception as e:
            print(f"Error reading file with ISO-8859-1 encoding {file_path}: {str(e)}")
            return None
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")
        return None


def load_model():
    return joblib.load('lease_clause_classifier.pkl')


def load_vectorizer():
    return joblib.load('tfidf_vectorizer.pkl')
