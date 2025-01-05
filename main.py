import streamlit as st
import json
from utils.textextractor import Utils  # Import Utils for text extraction
from builder.pipeline_builder import PipelineBuilder  # Import PipelineBuilder

# Initialize the PipelineBuilder
builder = PipelineBuilder()

# Streamlit interface
st.title("AI Mentalist and Pipeline Builder")

# Section 1: User Query Input
st.subheader("Step 1: Enter Your Query")
user_query = st.text_area(
    "Describe your task (e.g., 'Summarize this document').",
    placeholder="E.g., Summarize the key points of the uploaded document."
)

# Section 2: File Upload
st.subheader("Step 2: Upload Document (Optional)")
uploaded_file = st.file_uploader("Upload a PDF, TXT, or Word document", type=["pdf", "txt", "docx", "rtf"])

# Extract text from the uploaded file if provided
extracted_text = ""
if uploaded_file:
    file_type = uploaded_file.name.split(".")[-1].lower()
    if file_type == "pdf":
        extracted_text = Utils.extract_text_from_pdf(uploaded_file)
    elif file_type in ["docx", "rtf"]:
        extracted_text = Utils.extract_text_from_word(uploaded_file)
    elif file_type == "txt":
        extracted_text = uploaded_file.read().decode("utf-8")
    st.subheader("Extracted Text:")
    st.text_area("Text from Uploaded File:", value=extracted_text, height=200)

# Section 3: Refined Query
st.subheader("Step 3: Refine Your Query")
refined_query = st.text_area(
    "Enter the refined query (based on your task and extracted content):",
    placeholder="E.g., Summarize the key points of the document and focus on financial insights."
)

# Section 4: Specifications
st.subheader("Step 4: Specifications")
default_specifications = {
    "inputs": [{"name": "Document", "type": "text"}],
    "outputs": [{"name": "Summary", "type": "text"}]
}
specifications = st.text_area(
    "Enter the extracted specifications (in JSON format):",
    value=json.dumps(default_specifications, indent=2),
    height=200
)

# Generate Pipeline
if st.button("Generate Pipeline"):
    try:
        # Parse the specifications from JSON
        specs = json.loads(specifications)

        # Call the PipelineBuilder to generate the pipeline
        full_pipeline = builder.generate_pipeline(user_query, refined_query, specs)

        st.subheader("Generated Pipeline Graph (JSON):")
        st.json(full_pipeline)
    except Exception as e:
        st.error(f"Error: {str(e)}")
