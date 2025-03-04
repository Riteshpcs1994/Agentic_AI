from agentic_ai.src.prompt import classify_query, sql_agent_query
from agentic_ai.src.decision_making_agent_prompt import (
    get_classification, custom_llm_model, RAG_agent, sql_query_result
)
import gradio as gr
import json
import datetime


custom_llm = custom_llm_model()

chat_memory = []

def log_query(user_query, response):
    log_entry = {
        "timestamp": str(datetime.datetime.now()),
        "query": user_query,
        "response": response
    }
    with open("chat_logs.json", "a") as log_file:
        log_file.write(json.dumps(log_entry) + "\n")

# Function to Handle Chat with Memory
def agentx_response(query, history):
    global chat_memory

    query_format = classify_query(query)
    query_classification = get_classification(query_format)
    query_type = query_classification["query_type"]

    if query_type == '1':
        print("General LLM Intelligence used")
        answer = custom_llm.invoke(f"[INST] {query} [/INST]")

    elif query_type == '2':
        print("Company's internal Project-base searched")
        answer = RAG_agent(query)

    else:
        print("Searching in company's database")
        sql_query = custom_llm.invoke(sql_agent_query(query))
        answer = sql_query_result(sql_query)

    # Update Memory & Log Query
    chat_memory.append({"user": query, "agent": answer})
    log_query(query, answer)

    return answer

# Gradio Chatbot UI
chatbot = gr.ChatInterface(agentx_response, title="QueryMind", description="Ask me anything!")

# Launch the App
if __name__ == "__main__":
    chatbot.launch()
