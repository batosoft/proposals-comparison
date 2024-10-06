---

# 🚀 **RFP Proposal Comparison App Using Generative AI**

## 📚 **Overview**

This project is a cutting-edge **Generative AI-powered** application that streamlines the evaluation process of proposals submitted in response to **Requests for Proposals (RFPs)**. The app leverages **Natural Language Processing (NLP)** techniques to analyze and summarize proposals, compare them based on specific criteria, and generate comprehensive reports to assist decision-makers in selecting the most suitable proposal efficiently.

The app is designed to save time, improve decision-making accuracy, and provide an intuitive experience for users. With features like uploading proposal PDFs, generating comparison reports, and downloading results as PDFs, the application brings the power of AI into the business workflow.

---

## 🎯 **Key Features**

- **PDF Uploads**: Upload RFP and proposal documents in PDF format.
- **AI-powered Summarization**: Automatically summarizes key sections of each proposal using advanced **Generative AI** models.
- **Comparison Reports**: The app compares two proposals based on the specific requirements outlined in the RFP, identifying key differentiators.
- **Downloadable PDF Reports**: Export the comparison results as a downloadable PDF report for further review.
- **User-friendly Interface**: Built using **Gradio**, offering an easy-to-use interface for non-technical users.

---

## 🛠 **Technology Stack**

- **Backend**:
  - Python 3.x
  - **Hugging Face Transformers** for text summarization (`distilbart-cnn-12-6`)
  - **PyPDF2** for PDF text extraction
  - **fpdf** for PDF report generation

- **Frontend**:
  - **Gradio**: A simple, interactive interface to upload PDFs and download the comparison results.

- **AI Model**:
  - **DistilBART**: Pre-trained transformer-based summarization model for condensing lengthy proposals into concise summaries.

---

## 📑 **How It Works**

1. **Upload RFP and Proposal PDFs**: The app accepts the RFP and two proposal documents in PDF format.
2. **AI Summarization**: Using **NLP**, the text is extracted and passed through a summarization model to generate concise versions of each proposal.
3. **Comparison**: The app compares both proposals based on specific criteria derived from the RFP.
4. **Generate Report**: A comparison report is generated, highlighting key differences between the proposals and providing recommendations.
5. **Download Report**: Users can download the report in PDF format for further analysis and approval.

---

## 🚀 **Getting Started**

### **Installation**

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/proposal-comparison-gai.git
    cd proposal-comparison-gai
    ```

2. **Set up a virtual environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Download model dependencies**:
    Make sure PyTorch or TensorFlow is installed to use the summarization models. Follow the instructions here:
    - [PyTorch Installation](https://pytorch.org/get-started/locally/)
    - [TensorFlow Installation](https://www.tensorflow.org/install)

5. **Run the app**:
    ```bash
    python Proposals.py
    ```

6. Open your browser and go to the link provided by Gradio to start using the app.

---

## 🧠 **Model Used**

- **DistilBART (Distilled BART)**: This model is a smaller, faster variant of the BART model, trained specifically for **text summarization**. It reduces the length of input documents while maintaining key details and context, making it perfect for summarizing RFPs and proposals.

---

## 💡 **Project Structure**

```
.
├── Proposals.py          # Main application script
├── requirements.txt      # Required dependencies
├── README.md             # Project README
└── .venv/                # Virtual environment (created after setup)
```

---

## ⚙️ **Preprocessing Steps**

The text extracted from the PDFs undergoes the following steps:
1. **PDF Parsing**: Using `PyPDF2`, the content is extracted from the RFP and proposal documents.
2. **Summarization**: The extracted text is summarized using the `distilbart-cnn-12-6` model, providing a condensed version for easier comparison.
3. **Comparison**: The summaries are analyzed against the criteria in the RFP, and the most significant differentiators between proposals are highlighted.

---

## 🔧 **Challenges Encountered**

- **PDF Text Extraction**: Handling complex PDFs with tables, charts, and other non-text elements.
- **Model Accuracy**: Ensuring the summarization retains all important technical details.
- **Performance**: Optimizing the AI model for large, complex proposals.

---

## 📜 **Future Improvements**

- **Enhanced PDF Parsing**: Support for more complex document structures such as tables, images, and multi-column text.
- **Customizable Summarization**: Allow users to control the level of detail in summaries.
- **Multi-proposal Comparison**: Extend the comparison to handle more than two proposals at once.

---

## 🤝 **Contributing**

We welcome contributions! If you want to contribute to the project, feel free to create a fork, submit pull requests, or raise issues. Please follow the standard GitHub practices for collaboration.

---

## 📄 **License**

This project is licensed under the [MIT License](LICENSE).

---

## 📧 **Contact**

If you have any questions or suggestions, feel free to reach out to me via batosoft3@gmail.com.

---

This README provides an in-depth overview, technical insights, and a clear setup guide for users and contributors. You can adapt it based on your project’s updates or new features!
