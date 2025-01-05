from openai import OpenAI
import json
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
)

class PipelineBuilder:
    def __init__(self):
        """
        Initialize the PipelineBuilder
        """
        pass

    def generate_branch(self, user_query, refined_query, input_node, output_node, existing_nodes, existing_edges):
        """
        Generates a single branch of the pipeline graph between the input and output nodes, using the user and refined queries for context.

        Args:
            user_query (str): The initial user query.
            refined_query (str): The clarified and refined query.
            input_node (str): The name of the input node.
            output_node (str): The name of the output node.
            existing_nodes (list): List of existing nodes to avoid redundancy.
            existing_edges (list): List of existing edges to avoid redundancy.

        Returns:
            dict: A partial pipeline graph for the specific branch.
        """
        # Example pipeline prompt for GPT-4o
        system_message = (
            "You are an AI Pipeline Builder specializing in generating subgraphs (branches) of a larger pipeline. "
            "Use the provided user query and refined query to guide your pipeline generation."
        )

        examples = '''
            Examples of Pipelines for Different Types of Queries:

            1. Document Summary:
            User Query: "Summarize the key points of the document."
            Pipeline Output:
            {{
            "nodes": [
                {{"id": "1", "type": "input", "name": "Document", "modality": "text"}},
                {{"id": "2", "type": "function", "name": "Summarizer", "modality": "text-to-summary"}},
                {{"id": "3", "type": "output", "name": "Summary", "modality": "text"}}
            ],
            "edges": [
                {{"from": "1", "to": "2"}},
                {{"from": "2", "to": "3"}}
            ]
            }}

            2. Specific Query:
            User Query: "What are the revenue trends in the document?"
            Pipeline Output:
            {{
            "nodes": [
                {{"id": "1", "type": "input", "name": "Document", "modality": "text"}},
                {{"id": "2", "type": "function", "name": "Question Answering", "modality": "text-to-answer"}},
                {{"id": "3", "type": "output", "name": "Answer", "modality": "text"}}
            ],
            "edges": [
                {{"from": "1", "to": "2"}},
                {{"from": "2", "to": "3"}}
            ]
            }}

            3. Section-Specific Query:
            User Query: "Explain the financials in Section 3."
            Pipeline Output:
            {{
            "nodes": [
                {{"id": "1", "type": "input", "name": "Document", "modality": "text"}},
                {{"id": "2", "type": "function", "name": "Section Extractor", "parameters": {{"section": "3"}}}},
                {{"id": "3", "type": "function", "name": "Summarizer", "modality": "text-to-summary"}},
                {{"id": "4", "type": "output", "name": "Summary of Section 3", "modality": "text"}}
            ],
            "edges": [
                {{"from": "1", "to": "2"}},
                {{"from": "2", "to": "3"}},
                {{"from": "3", "to": "4"}}
            ]
            }}

            4. Actionable Query:
            User Query: "Generate a bar chart of sales figures."
            Pipeline Output:
            {{
            "nodes": [
                {{"id": "1", "type": "input", "name": "Document", "modality": "text"}},
                {{"id": "2", "type": "function", "name": "Data Extractor", "parameters": {{"data_type": "sales figures"}}}},
                {{"id": "3", "type": "function", "name": "Chart Generator", "parameters": {{"chart_type": "bar"}}}},
                {{"id": "4", "type": "output", "name": "Bar Chart", "modality": "image"}}
            ],
            "edges": [
                {{"from": "1", "to": "2"}},
                {{"from": "2", "to": "3"}},
                {{"from": "3", "to": "4"}}
            ]
            }}

            5. Generate New Content:
            User Query: "Create a marketing campaign for this product."
            Pipeline Output:
            {{
            "nodes": [
                {{"id": "1", "type": "input", "name": "Document", "modality": "text"}},
                {{"id": "2", "type": "function", "name": "Content Generator", "parameters": {{"content_type": "marketing campaign"}}}},
                {{"id": "3", "type": "output", "name": "Marketing Campaign", "modality": "text"}}
            ],
            "edges": [
                {{"from": "1", "to": "2"}},
                {{"from": "2", "to": "3"}}
            ]
            }}

            Now, generate a pipeline for the provided query.
        '''
        user_prompt = f"""
            You are an advanced AI Pipeline Builder that generates pipeline subgraphs based on user queries and document content. 
            For the provided user query, refined query, and document specifications, construct a sub graph in JSON format.

            User Query: {user_query}

            Refined Query: {refined_query}

            Input Node: {input_node}
            Output Node: {output_node}

            Existing Nodes:
            {json.dumps(existing_nodes, indent=2)}

            Existing Edges:
            {json.dumps(existing_edges, indent=2)}

            {examples}

            Ensure the generated branch:
            - Aligns with the refined query.
            - Reuses existing nodes and edges where applicable.
            - Clearly defines all new nodes and edges.

            Output the result in JSON format.
            
            """

        # Call GPT-4o to generate the pipeline
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )

        print(response.choices[0])

        response_content = response.choices[0].message.content.strip()

        if response_content.startswith("```json"):
            response_content = response_content.strip("```json").strip("```").strip()

        try:
            branch = json.loads(response_content)
            return branch
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse response as JSON: {response_content}") from e
    
    def generate_pipeline(self, user_query, refined_query, specifications):
        """
        Generates the full pipeline by combining branches for each input-output pair in the specifications.

        Args:
            refined_query (str): The clarified and refined query.
            specifications (dict): Contains input and output specifications.

        Returns:
            dict: Full pipeline graph.
        """
        full_pipeline = {"nodes": [], "edges": []}
        node_ids = set()
        existing_nodes = []
        existing_edges = []

        for input_spec in specifications["inputs"]:
            for output_spec in specifications["outputs"]:
                branch = self.generate_branch(user_query, refined_query, input_spec, output_spec, existing_nodes, existing_edges)
                
                # Merge the branch into the full pipeline
                for node in branch["nodes"]:
                    if node["id"] not in node_ids:
                        full_pipeline["nodes"].append(node)
                        node_ids.add(node["id"])
                        existing_nodes.append(node)
                for edge in branch["edges"]:
                    if edge not in full_pipeline["edges"]:
                        full_pipeline["edges"].append(edge)
                        existing_edges.append(edge)

        return full_pipeline