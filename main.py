#from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

import gradio as gr

import os
from os.path import join, dirname
from dotenv import load_dotenv


# Loading the environment variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Initialize the LLM model
llm = ChatOpenAI(temperature=0, model=os.environ.get('OPENAI_MODEL'), api_key=os.environ.get('OPENAI_API_KEY'), base_url=os.environ.get('OPENAI_API_HOST'))  # type: ignore

# Step 1: Load and Split Document
def load_and_split_document(filepath):
    loader = PyPDFLoader(filepath)
    documents = loader.load_and_split()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    text_chunks = splitter.split_documents(documents)
    return text_chunks

# Step 2: Grammar Correction Node
def correct_grammar(text):
    grammar_prompt_message = """
    Correct the following text for grammar mistakes:
    {text}
    """
    grammar_prompt = PromptTemplate(
        input_variables=["text"],
        template=grammar_prompt_message,
    )
    
    # Output Parser
    output_parser=StrOutputParser()
    
    chain = grammar_prompt | llm | output_parser
    result = chain.invoke(input={"text": text}) 
    return result

# Step 3: Rewriting Node based on user selection
def rewrite_text(text, style):
    style_map = {
        "Standard": "a standard, well-structured",
        "Natural": "a human, conversational",
        "Formal": "a formal, professional",
        "Fluency": "a fluent, clear"
    }
    selected_style = style_map.get(style, "standard")
    rewrite_prompt_message = """
    Rewrite the following text in {style} style:
    {text}
    """
    rewrite_prompt = PromptTemplate(
        input_variables=["text","style"],
        template=rewrite_prompt_message,
    )
    # Output Parser
    output_parser=StrOutputParser()

    chain = rewrite_prompt | llm | output_parser
    result = chain.invoke(input={"text": text, "style": selected_style}) # type: ignore
    return result

# Step 4: Create LangGraph Nodes
def process_pdf(filepath, output_type):
    # Step 1: Load Document
    document_chunks = load_and_split_document(filepath)
    
    # Step 2: Get the page content
    page_content = " "
    for i, chunk in enumerate(document_chunks):
        page_content = page_content + chunk.page_content
    
    # Step 3: Define a list of runnable tasks
    runnable_tasks = {
        f"task_{i}": (lambda chunk=chunk: rewrite_text(correct_grammar(page_content), output_type))
        for i, chunk in enumerate(document_chunks)
    }

    # Step 4: LangGraph parallel processing
    parallel_chain = RunnableParallel(runnable_tasks) # type: ignore
    
    # Step 5: Execute the chain and merge results
    results = parallel_chain.invoke(input={}) # type: ignore
        
    return results['task_0']


# Step 5: Process User-Entered Text
def process_text(user_input_text, output_type):
    # Grammar Correction and Rewriting for the entered text
    corrected_text = correct_grammar(user_input_text)
    rewritten_text = rewrite_text(corrected_text, output_type)
    return rewritten_text

# Function to handle both input types based on user selection
def document_correction_interface(input_mode, file=None, text_input=None, output_type=None):
    if input_mode == "PDF File" and file is not None:
        return process_pdf(file.name, output_type) # type: ignore
    elif input_mode == "Text Input" and text_input is not None:
        return process_text(text_input, output_type)
    else:
        return "Please select an input mode and provide the corresponding data."

# Gradio Interface
def process_document(input_mode, file, text_input, output_type):
    return document_correction_interface(input_mode, file, text_input, output_type)

# Gradio UI
def main_ui():
    interface = gr.Interface(
    fn=process_document,
    inputs=[
        gr.Radio(choices=["PDF File", "Text Input"], label="Select Input Mode"),  # Input mode selection
        gr.File(label="Upload PDF File"),  # PDF file input (hidden by default)
        gr.Textbox(label="Enter Text"),  # Text input box (hidden by default)
        gr.Dropdown(["Standard", "Natural", "Formal", "Fluency"], label="Select Output Style")  # Output style selection
    ],
    outputs="text",
    title="Document Correction Application",
    description="Upload a PDF file or enter text, and select the style to correct grammar and rewrite it.",
    )

    # Launch the Gradio interface
    interface.launch()

# Run the application
if __name__ == "__main__":
    main_ui()