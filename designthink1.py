import requests
import fitz  # PyMuPDF
from fpdf import FPDF
import os

# API Credentials
API_KEY = "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"
API_URL = "https://api.groq.com/openai/v1/chat/completions"

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    try:
        doc = fitz.open(pdf_path)
        text = "\n".join(page.get_text("text") for page in doc)
        return text.strip()
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return ""

def generate_questions(text):
    """Generates categorized questions using an AI model."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "You are an AI tutor that generates categorized questions from text."},
            {"role": "user", "content": f"Generate categorized questions from the following text in this format:\n\n"
                                       "Part A (Remember)\n"
                                       "1. Question...\n"
                                       "2. Question...\n"
                                       "3. Question...\n"
                                       "\n"
                                       "Part B (Understand)\n"
                                       "4. Question...\n"
                                       "5. Question...\n"
                                       "6. Question...\n"
                                       "\n"
                                       "Part C (Apply)\n"
                                       "7. Question...\n"
                                       "8. Question...\n"
                                       "9. Question...\n"
                                       f"\nText:\n{text}"}
        ],
        "temperature": 0.7,
        "max_tokens": 700
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()  # Raises an error for non-200 responses
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        print(f"❌ API Error: {e}")
        return "Error generating questions"

def create_question_paper(questions, details, logo_path=None):
    """Creates a formatted question paper in PDF format."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 12)

    # Add logo if it exists
    if logo_path and os.path.exists(logo_path):
        try:
            pdf.image(logo_path, 10, 10, 30)
        except:
            print("⚠️ Warning: Unable to load logo. Proceeding without it.")

    # College Name and Exam Title
    pdf.cell(0, 10, details['college'], ln=True, align='C')
    pdf.cell(0, 10, details['exam_title'], ln=True, align='C')
    pdf.ln(5)

    # Table for Exam Details
    pdf.set_font("Arial", "B", 10)
    column_width = 50
    row_height = 8
    pdf.cell(column_width, row_height, f"Course Code: {details['course_code']}", border=1, ln=False, align="C")
    pdf.cell(column_width, row_height, f"Course Name: {details['course_name']}", border=1, ln=False, align="C")
    pdf.cell(column_width, row_height, f"Faculty: {details['faculty']}", border=1, ln=True, align="C")

    pdf.cell(column_width, row_height, f"Date: {details['date']}", border=1, ln=False, align="C")
    pdf.cell(column_width, row_height, f"Duration: {details['duration']}", border=1, ln=False, align="C")
    pdf.cell(column_width, row_height, f"Semester: {details['semester']}", border=1, ln=True, align="C")

    pdf.cell(column_width, row_height, f"Max Marks: {details['max_marks']}", border=1, ln=True, align="C")
    pdf.ln(10)

    # Section Heading
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 8, "Answer All Questions", ln=True, align='L')
    pdf.ln(5)
    
    # Add questions
    pdf.set_font("Arial", "", 10)
    sections = questions.split("\n\n")
    for section in sections:
        pdf.set_font("Arial", "B", 10)
        pdf.multi_cell(0, 8, section.split("\n")[0], align='L')
        pdf.ln(2)
        pdf.set_font("Arial", "", 10)
        for line in section.split("\n")[1:]:
            pdf.multi_cell(0, 6, line, align='L')
            pdf.ln(1)
        pdf.ln(5)

    output_path = "Generated_Question_Paper.pdf"
    pdf.output(output_path)
    print(f"✅ PDF Saved as {output_path}")

# Collect exam details
details = {
    'college': input("Enter College Name: "),
    'exam_title': input("Enter Exam Title: "),
    'course_code': input("Enter Course Code: "),
    'course_name': input("Enter Course Name: "),
    'faculty': input("Enter Faculty Name: "),
    'semester': input("Enter Semester: "),
    'max_marks': input("Enter Max Marks: "),
    'date': input("Enter Date: "),
    'duration': input("Enter Duration: ")
}

pdf_path = input("Enter Curriculum PDF Path: ")

# Check if PDF exists
if not os.path.exists(pdf_path):
    print("❌ Error: PDF file not found.")
else:
    extracted_text = extract_text_from_pdf(pdf_path)
    if extracted_text:
        questions = generate_questions(extracted_text)
        if questions != "Error generating questions":
            logo_path = input("Enter Logo Path (Leave blank if none): ").strip()
            create_question_paper(questions, details, logo_path)
        else:
            print("❌ Failed to generate questions.")
    else:
        print("❌ Failed to extract text from PDF.")
