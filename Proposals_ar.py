import gradio as gr
import pandas as pd
import PyPDF2
from fpdf import FPDF
from transformers import pipeline

# Load a text summarization model from Hugging Face (supports Arabic)
summarizer = pipeline("summarization", model="facebook/mbart-large-50-many-to-many-mmt")

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to analyze proposals
def analyze_proposals(proposal1_text, proposal2_text, criteria):
    # Summarize both proposals
    summary1 = summarizer(proposal1_text, max_length=150, min_length=50, do_sample=False)[0]['summary_text']
    summary2 = summarizer(proposal2_text, max_length=150, min_length=50, do_sample=False)[0]['summary_text']
    
    # Compare proposals based on criteria
    comparison = f"### المقارنة بناءً على المعايير: {criteria}\n"
    comparison += f"- **ملخص المقترح 1**: {summary1}\n"
    comparison += f"- **ملخص المقترح 2**: {summary2}\n"
    
    # Generate a simple recommendation based on length
    if len(summary1) > len(summary2):
        recommendation = "يبدو أن المقترح 1 أكثر تفصيلاً."
    else:
        recommendation = "يبدو أن المقترح 2 أكثر تفصيلاً."
    
    return comparison, recommendation

# Function to generate PDF report
def generate_pdf(proposal1_text, proposal2_text, comparison, recommendation, criteria):
    pdf = FPDF()
    pdf.add_page()
    
    # Set title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="تقرير مقارنة المقترحات", ln=True, align='C')
    
    # Add Criteria
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"المعايير: {criteria}", ln=True, align='L')
    
    # Add Proposal 1 and Proposal 2
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="المقترح 1:", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(200, 10, txt=proposal1_text)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="المقترح 2:", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(200, 10, txt=proposal2_text)
    
    # Add Comparison and Recommendation
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="المقارنة:", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(200, 10, txt=comparison)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="التوصية:", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(200, 10, txt=recommendation)
    
    # Save the PDF
    pdf_output_path = "data/proposal_comparison_report.pdf"
    pdf.output(pdf_output_path)
    
    return pdf_output_path

# Set up the Gradio Interface
def interface():
    with gr.Blocks() as app:
        gr.Markdown("<h1 style='text-align:right'>أداة مقارنة المقترحات باستخدام الذكاء الاصطناعي التوليدي</h1>")

        with gr.Row():
            rfp_input = gr.File(label="تحميل طلب تقديم العروض (PDF)", elem_id="rtl")
            proposal1_input = gr.File(label="تحميل المقترح 1 (PDF)", elem_id="rtl")
            proposal2_input = gr.File(label="تحميل المقترح 2 (PDF)", elem_id="rtl")
        
        criteria_input = gr.Textbox(label="معايير المقارنة", placeholder="أدخل المعايير الرئيسية للمقارنة", lines=2, elem_id="rtl")
        
        compare_btn = gr.Button("مقارنة المقترحات", elem_id="rtl")
        download_btn = gr.Button("تحميل تقرير PDF", elem_id="rtl")
        
        comparison_output = gr.Textbox(label="نتائج المقارنة", interactive=False, lines=10, elem_id="rtl")
        recommendation_output = gr.Textbox(label="التوصية", interactive=False, lines=2, elem_id="rtl")
        download_link = gr.File(label="تحميل التقرير", interactive=False, elem_id="rtl")
        
        # Define what happens when the "Compare" button is clicked
        def on_compare(rfp, proposal1, proposal2, criteria):
            rfp_text = extract_text_from_pdf(rfp) if rfp else ""
            proposal1_text = extract_text_from_pdf(proposal1)
            proposal2_text = extract_text_from_pdf(proposal2)
            
            comparison, recommendation = analyze_proposals(proposal1_text, proposal2_text, criteria)
            return comparison, recommendation
        
        # Define what happens when the "Download PDF Report" button is clicked
        def on_download(rfp, proposal1, proposal2, criteria):
            rfp_text = extract_text_from_pdf(rfp) if rfp else ""
            proposal1_text = extract_text_from_pdf(proposal1)
            proposal2_text = extract_text_from_pdf(proposal2)
            comparison, recommendation = analyze_proposals(proposal1_text, proposal2_text, criteria)
            pdf_path = generate_pdf(proposal1_text, proposal2_text, comparison, recommendation, criteria)
            return pdf_path
        
        compare_btn.click(on_compare, inputs=[rfp_input, proposal1_input, proposal2_input, criteria_input], outputs=[comparison_output, recommendation_output])
        download_btn.click(on_download, inputs=[rfp_input, proposal1_input, proposal2_input, criteria_input], outputs=download_link)

    return app

# Launch the app
if __name__ == "__main__":
    interface().launch()
