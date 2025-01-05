import streamlit as st
from builder.pipeline_builder import PipelineBuilder
from utils.textextractor import Utils  # Import Utils

# Initialize the PipelineBuilder
builder = PipelineBuilder()

# Task Classification Function
def classify_task(user_input):
    user_input = user_input.lower()
    if "summarize" in user_input or "summary" in user_input:
        return "Summarize"
    elif "what" in user_input or "explain" in user_input or "insight" in user_input:
        return "Answer Query"
    elif "translate" in user_input:
        return "Translate"
    elif "extract" in user_input:
        return "Extract Information"
    elif "generate" in user_input or "create" in user_input:
        return "Generate Content"
    else:
        return "Unknown Task"

# Step 1: Ask the user for their query
st.title("Bel Esprit Framework")
st.subheader("Step 1: What do you want to do?")
user_input = st.text_area("Enter your task or query:", placeholder="E.g., Summarize the key points of this document.")


# Initialize variables
task_type = None
input_language = None
text_content = None
output_format = None

# Step 2: Automatically classify the task
if user_input:
    task_type = classify_task(user_input)
    st.subheader("Detected Task")
    st.write(f"The system has classified your task as: **{task_type}**")
else:
    task_type = None

# Step 3: Ask for the language of the input
if task_type:
    st.subheader("Step 2: What is the language of your input?")
    input_language = st.text_input(
        "Enter the language of the input text (e.g., English, Spanish, etc.):",
        placeholder="E.g., English"
    )

    have_document = "No"

    # Step 4: Provide the text content
    if input_language:
        st.subheader("Step 3: Do you have a document to process?")
        if st.button("Yes"):
            have_document = "Yes"
        if st.button("No"):
            have_document = "No"

        st.subheader("Step 4: Define the Output Format")
        output_format = "Answer" if task_type == "Answer Query" else task_type

        st.write(f"Based on your task, the output format will be: **{output_format}**.")

    # Step 6: Build the pipeline
    if st.button("Build Pipeline"):
        if task_type and input_language and output_format:
            # Define specifications
            specifications = {
                "inputs": [
                    {
                        "name": "Text Content",
                        "type": "text",
                        "language": input_language,
                        "content": text_content
                    }
                ],
                "task": task_type,
                "outputs": [
                    {
                        "name": "Result",
                        "type": output_format.lower(),
                        "language": input_language
                    }
                ]
            }

            if have_document == "Yes":
                specifications["inputs"].append({
                    "name": "File Upload",
                    "type": "file",
                    "language": input_language,
                })

            # Generate the pipeline
            full_pipeline = builder.generate_pipeline(
                user_query=user_input,
                refined_query=f"Perform {task_type.lower()} on the given {input_language} text and produce a {output_format.lower()} as output.",
                specifications=specifications
            )

            st.subheader("Generated Pipeline")
            st.json(full_pipeline)

            st.success("Pipeline built successfully! You can now execute the pipeline.")
        else:
            st.error("Please complete all fields before building the pipeline.")
