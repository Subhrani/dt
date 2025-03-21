import requests
import pymupdf  # PyMuPDF
fitz=pymupdf
from fpdf import FPDF

API_KEY = "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"
API_URL = "https://api.groq.com/openai/v1/chat/completions"

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text("text") + "\n"
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
    
    response = requests.post(API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        print(f"❌ API Error: {response.json()}")
        return "Error generating questions"

def create_question_paper(questions, details, logo_path=r"C:\Users\SUBHA\Downloads\designthinking\LOGO.jpg"):
    """Creates a formatted question paper in PDF format."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 12)

    # Add default logo (if exists)
    if logo_path and logo_path.strip():
        try:
            pdf.image(logo_path, 10, 10, 30)
        except:
            print("⚠️ Warning: Unable to load logo. Proceeding without it.")

    pdf.cell(0, 10, details['college'], ln=True, align='C')
    pdf.cell(0, 10, details['exam_title'], ln=True, align='C')
    pdf.ln(5)

    # Table-like structure for exam details
    pdf.set_font("Arial", "B", 10)
    column_width = 45
    pdf.cell(column_width, 8, f"Course code: {details['course_code']}", border=1, ln=False, align="C")
    pdf.cell(column_width, 8, f"Course name: {details['course_name']}", border=1, ln=False, align="C")
    pdf.cell(column_width, 8, f"Faculty: {details['faculty']}", border=1, ln=False, align="C")
    pdf.cell(column_width, 8, f"Date: {details['date']}", border=1, ln=True, align="C")
    pdf.cell(column_width, 8, f"Duration: {details['duration']}", border=1, ln=False, align="C")
    pdf.cell(column_width, 8, f"Semester: {details['semester']}", border=1, ln=False, align="C")
    pdf.cell(column_width, 8, f"Max Marks: {details['max_marks']}", border=1, ln=True, align="C")
    pdf.ln(10)

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

    pdf.output("Generated_Question_Paper.pdf")
    print("✅ PDF Saved as Generated_Question_Paper.pdf")

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

# Process
extracted_text = extract_text_from_pdf(pdf_path)
questions = generate_questions(extracted_text)
create_question_paper(questions, details)

