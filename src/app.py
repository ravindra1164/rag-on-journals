import streamlit as st
#from langchain_ollama.llms import OllamaLLM
#from langchain_ollama import ChatOllama
from langchain.tools import tool
#from langchain.messages import AIMessage, HumanMessage, ToolMessage, SystemMessage
#from langchain_core.prompts import ChatPromptTemplate
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
#from langchain_mcp_adapters.tools import load_mcp_tools
from vector import retriever
import asyncio

@tool(
        response_format="content", 
        description="Get relevant reviews for a given query. Use this to find information about the restaurant based on customer feedback."
)
def get_relavent_reviews(user_query: str):
    """Retrieve information to help answer a query."""
    reviews = retriever.invoke(user_query)
    return reviews

def main():
    prompt = """
        You are an exeprt in answering questions about a pizza restaurant. 
        
        You can also call tools to get reviews."""
    
    client = MultiServerMCPClient(
        {
            "JournalsMCPServer": {
                "transport": "http",
                "url": "http://localhost:8000/mcp",
                "headers": {
                    "Authorization": "Bearer YOUR_TOKEN",
                    "X-Custom-Header": "custom-value"
                },
            }
        }
    )
    mcp_tools = client.get_tools()
    lc_tools = [get_relavent_reviews]
    print("MCP Tools:", mcp_tools)
    print("Langchain Tools:", lc_tools)
    tools = mcp_tools+lc_tools
    agent = create_agent(
        model="ollama:qwen3.5:0.8b",
        tools=tools,
        system_prompt=prompt
    )

    #message = {"role": "user", "messages": "Greet User Ravi"}
    #response_full = await agent.ainvoke(message)
    #for response in response_full.get('messages') :
    #    print("Message type : ", response.type)
    #    print(response)     
    #exit()



    #llm = ChatOllama(
    #    model="qwen3.5:0.8b",
    #    temperature=0.7
    #).bind_tools(tools)
    #template = """
    #    You are an exeprt in answering questions about a pizza restaurant. 
        
    #    You can also call tools to get customn greeting to user.

    #    Here are some relevant reviews: {reviews}

    #    Here is the question to answer: {question}"""
    #prompt = ChatPromptTemplate.from_template(template)
    #chain = prompt | agent

    st.title("Simple Streamlit Chat App")

    prompt = st.text_input("Enter your question:", value="Are the pizzas good?")
    if st.button("Ask"):
        with st.spinner("Getting answer..."):
            message = {"role": "user", "messages": prompt}
            response_full = agent.ainvoke(message)
            st.success("Response received!")
            st.write(response_full)
            #for response in response_full.get('messages') :
                #print("Message type : ", response.type)
                #print(response)
                #if response.type == "tool":
                #    st.write(response.content[0].get('text'))
                #el
             #   if response.type == "ai":
             #       st.write(response.content)
            
            #reviews = retriever.invoke(prompt)
            #result = chain.invoke({"reviews": reviews, "question": prompt})



    #result = llm.invoke(
    #    "Hi"
    #)
    #print("LLM response:")
    #print(result)
    #agent = create_agent(
    #    model="ollama:smollm2:135m", 
    #    tools=tools
    #)
    
    #print("Invoking agent...")
    #response = await agent.ainvoke(
    #    {"messages": [{"role": "user", "content": "Greet User Ravi"}]}    
    #)
    #print("Agent response:")
    #print(response)
    #print("Done.")

if __name__ == "__main__":
    main() 