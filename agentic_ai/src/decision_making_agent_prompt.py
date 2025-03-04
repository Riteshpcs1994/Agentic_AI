from langchain.chains import RetrievalQA
import re
import json
import sqlite3

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores import Chroma
import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from langchain.llms import HuggingFacePipeline
from transformers import pipeline
# Prompt for Decision Maker Agent

torch.set_default_device("mps")

def custom_llm_model():
    device = "mps" if torch.backends.mps else "cpu"
    model_name = "mistralai/Mistral-7B-Instruct-v0.1"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")

    hf_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=100,  # Adjust for faster responses
        temperature=0.1,  # Makes output more deterministic
        top_p=0.95,  # Controls randomness
        do_sample=True,
        return_full_text=False,
        pad_token_id=tokenizer.eos_token_id
    )

    custom_llm = HuggingFacePipeline(pipeline=hf_pipeline)
    return custom_llm

    
def get_classification(prompt):
    # Generate prompt
    custom_llm = custom_llm_model()
    outputs = custom_llm.invoke(prompt)
    result = json.loads(outputs)
    return result
    
 # SQl Agent
def sql_query_result(res):
    """
    Decodes the JSON response to extract a SQL query and executes it.

    Parameters:
        res (str): The raw response from the LLM API.
        cursor: Database cursor object for executing the query.

    Returns:
        list: A list of rows resulting from the executed query.
    """
    data_base_path = os.path.abspath("agentic_ai/data/employee.db")
    conn = sqlite3.connect(data_base_path)
    cursor = conn.cursor()
    try:
        
        # print(f"Extracted JSON: {json_response}")

        # Parse the JSON response
        response_dict = json.loads(res.strip())
        
        # Validate that the query exists
        if "query" not in response_dict:
            raise ValueError("Invalid JSON structure: Missing 'query'.")
        
        # Extract and execute the SQL query
        sql_query = response_dict["query"].strip()
        if not sql_query:
            raise ValueError("Empty SQL query in the response.")

        print(f"Executing SQL Query: {sql_query}")
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        rows = [x[0] for x in rows]
        # Return the query result
        return rows

    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")
    except Exception as e:
        raise ValueError(f"An error occurred: {e}")


from langchain.prompts import PromptTemplate

def RAG_agent(query):
    # Define a custom prompt for the question-answering system

    prompt_template = """[INST] 
    You are a helpful assistant for Company XYZ. Your task is to answer questions based on the provided project documents.
    
    ### Documents:
    {context}

    ### Question:
    {question}

    If the documents contain relevant information, answer based only on them.
    If the documents do not provide an answer, say "The documents do not contain relevant information.
    [/INST]"""
    
    custom_llm = custom_llm_model()
    #path = os.path.abspath("agentic_ai/data/chroma_db")
    path = "/Users/ritkumar17/Desktop/R&D_Project/Agentic_AI/agentic_ai/data/chroma_db"
    embeddings_model = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en")
    knowledge_base = Chroma(persist_directory=path, embedding_function=embeddings_model)
    # Create a prompt template instance
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=prompt_template
    )
    
    # Use the prompt in the RetrievalQA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=custom_llm,
        retriever=knowledge_base.as_retriever(search_kwargs={"k": 5}),
        chain_type_kwargs={"prompt": prompt}
    )
    
    # Ask a question
    # query = "'Have we done anything on Air Quality improvement?',"
    response = qa_chain.run(query)
    #response = response.split("[/INST]")[-1].strip()
    return response