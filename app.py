import gradio as gr
import PyPDF2
from fpdf import FPDF
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import json
import os

# Load a lightweight Hugging Face summarization model
model_name = "sshleifer/distilbart-cnn-12-6"  # Faster and memory-efficient model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Function to summarize text using Hugging Face model
def summarize_text(text):
    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
    outputs = model.generate(inputs, max_length=150, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to analyze multiple proposals
def analyze_multiple_proposals(proposal_texts, criteria):
    summaries = []
    comparison = f"### Comparison based on the criteria: {criteria}\n"
    
    for i, text in enumerate(proposal_texts, start=1):
        summary = summarize_text(text)
        summaries.append(summary)
        comparison += f"- **Proposal {i} Summary**: {summary}\n"
    
    # Generate a simple recommendation based on length
    detailed_proposal = max(summaries, key=len)
    recommendation = f"The most detailed proposal is likely: Proposal {summaries.index(detailed_proposal) + 1}."
    
    return comparison, recommendation

# Function to generate PDF report
def generate_pdf(proposal_texts, comparison, recommendation, criteria):
    pdf = FPDF()
    pdf.add_page()
    
    # Set title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Proposal Comparison Report", ln=True, align='C')
    
    # Add Criteria
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"Criteria: {criteria}", ln=True, align='L')
    
    # Add each Proposal's text and summary
    for i, text in enumerate(proposal_texts, start=1):
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt=f"Proposal {i}:", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(200, 10, txt=text)
    
    # Add Comparison and Recommendation
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Comparison:", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(200, 10, txt=comparison)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Recommendation:", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(200, 10, txt=recommendation)
    
    # Save the PDF
    pdf_output_path = "data/proposal_comparison_report.pdf"
    pdf.output(pdf_output_path)
    
    return pdf_output_path

# Function to load language JSON based on the selected language
def load_language_data(language):
    lang_file_path = os.path.join("lang", f"{language.lower()}.json")
    with open(lang_file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# Function to update interface text based on language selection
def update_interface(language, components):
    lang_data = load_language_data(language)
    
    # Update content for components using 'value' instead of 'update'
    components["title"].value = lang_data["title"]
    components["rfp_label"].value = lang_data["rfp_label"]
    components["proposals_label"].value = lang_data["proposals_label"]
    components["criteria_label"].value = lang_data["criteria_label"]
    components["compare_btn"].value = lang_data["compare_btn"]
    components["download_btn"].value = lang_data["download_btn"]
    components["comparison_label"].value = lang_data["comparison_label"]
    components["recommendation_label"].value = lang_data["recommendation_label"]
    components["download_link_label"].value = lang_data["download_link_label"]
    
    # Apply RTL class directly to the container based on language
    if language in ["Arabic", "Hebrew"]:
        components["lang_container"].classes = "rtl"  # Apply RTL to the container
    else:
        components["lang_container"].classes = ""  # Remove RTL for LTR languages

# Set up the Gradio Interface
def interface():
    with gr.Blocks(css="public/style.css") as app:  # Adding the CSS file
        # Create a container for the language-related components
        lang_container = gr.Column()

        # Language Selector at the top
        language_selector = gr.Dropdown(choices=["English", "Arabic", "French", "Spanish"], label="Select Language", value="English")

        components = {
            "title": gr.Markdown(value="Generative AI RFP Proposal Comparison Tool"),
            "rfp_label": gr.File(label="Upload RFP (PDF)", file_types=[".pdf"], file_count="single"),
            "proposals_label": gr.File(label="Upload Proposals (PDF)", file_types=[".pdf"], file_count="multiple"),
            "criteria_label": gr.Textbox(label="Comparison Criteria", placeholder="Enter the key comparison criteria", lines=2),
            "compare_btn": gr.Button("Compare Proposals"),
            "comparison_label": gr.Textbox(label="Comparison Results", interactive=False, lines=10),
            "recommendation_label": gr.Textbox(label="Recommendation", interactive=False, lines=2),
            "download_btn": gr.Button("Download PDF Report"),
            "download_link_label": gr.File(label="Download Report", interactive=False),
            "lang_container": lang_container  # Adding the lang_container to components
        }

        # Update interface language based on the dropdown
        language_selector.change(fn=lambda language: update_interface(language, components), inputs=language_selector, outputs=[])

        # Define the actions for buttons
        def on_compare(rfp, proposals, criteria):
            rfp_text = extract_text_from_pdf(rfp) if rfp else ""
            proposal_texts = [extract_text_from_pdf(pdf) for pdf in proposals]
            comparison, recommendation = analyze_multiple_proposals(proposal_texts, criteria)
            pdf_output_path = generate_pdf(proposal_texts, comparison, recommendation, criteria)
            return comparison, recommendation, pdf_output_path

        # Set button action
        components["compare_btn"].click(fn=on_compare, inputs=[components["rfp_label"], components["proposals_label"], components["criteria_label"]], outputs=[components["comparison_label"], components["recommendation_label"], components["download_link_label"]])

        # File download button action
        components["download_link_label"].change(lambda file: file, inputs=components["download_link_label"], outputs=components["download_link_label"])

    app.launch(share=True)

interface()