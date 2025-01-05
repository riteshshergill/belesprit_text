# Bel Esprit Framework Implementation

This repository implements the **Bel Esprit Framework**, a modular and agent-based system designed to generate, validate, and refine complex AI pipelines. The framework leverages a chain-of-branches approach to decompose large graphs into smaller subgraphs, improving consistency and reducing errors.

For more details, refer to the white paper: [Bel Esprit Framework: Modular AI Pipeline Generation](https://arxiv.org/abs/2412.14684).

## Goals of the Bel Esprit Framework

The primary goal of the Bel Esprit Framework is to:
- **Simplify AI pipeline construction**: Break down complex graphs into smaller, manageable subgraphs.
- **Leverage LLMs for automation**: Use Large Language Models (LLMs) like GPT-4 to generate pipeline graphs dynamically based on user requirements.
- **Ensure semantic and syntactic accuracy**: Validate the generated graphs for structural correctness and alignment with user specifications.
- **Enhance adaptability**: Provide reusable and modular components that adapt to diverse AI tasks (e.g., summarization, insight extraction, content generation).

---

## Features

### Key Components

1. **Mentalist**: 
   - Refines ambiguous user queries.
   - Extracts structured specifications (inputs, outputs) from user queries and uploaded documents.

2. **PipelineBuilder**:
   - Generates pipeline subgraphs (branches) based on user queries, refined queries, and specifications.
   - Combines these subgraphs into a complete pipeline graph.

3. **Inspector** (future component):
   - Validates generated pipelines for structural and semantic alignment with user requirements.

---

## Recent Changes and Enhancements

### 1. **Mentalist Integration**
- Implemented a **Streamlit interface** to:
  - Allow users to input queries and refined tasks.
  - Upload documents (PDF, Word, or TXT) for content extraction.
  - Display extracted text and specifications.

### 2. **PipelineBuilder Enhancements**
- **Chain-of-Branches Approach**:
  - Generates subgraphs by focusing on input-output pairs derived from the specifications.
  - Each branch is semantically aligned with the refined query.

- **Example-Driven Prompting**:
  - Added multiple pipeline examples (e.g., document summarization, insight extraction, chart generation) to guide LLM outputs.

- **Handling LLM Outputs**:
  - Stripped Markdown-style code block delimiters (` ```json `) from LLM responses for proper JSON parsing.
  - Implemented error handling to catch and report invalid JSON outputs.

### 3. **Specifications-Based Subgraph Generation**
- Specifications provided by the user now dynamically define input-output pairs.
- Each subbranch (subgraph) is generated and then merged into the complete pipeline graph.

---

## Installation and Setup

### Prerequisites

- Python 3.8+
- OpenAI API key (requires GPT-4 access)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/riteshshergill/belesprit_text.git
   cd belesprit_text
