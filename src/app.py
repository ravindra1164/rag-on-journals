import streamlit as st
from langchain.tools import tool
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from vector import retriever
import asyncio


async def main():
    prompt = """
        You are an exeprt in answering questions about a pizza restaurant. 
        
        You can also call tools to get reviews."""
    
    client = MultiServerMCPClient(
        {
            "JournalsMCPServer": {
                "transport": "streamable-http",
                "url": "http://host.docker.internal:8000/mcp/",
                "headers": {
                    "Authorization": "Bearer YOUR_TOKEN",
                    "X-Custom-Header": "custom-value"
                },
            }
        }
    )
    mcp_tools = await client.get_tools()
    print("MCP Tools:", mcp_tools)

    @tool(
        response_format="content", 
        description="Get relevant reviews for a given query. Use this to find information about the restaurant based on customer feedback."
    )
    def get_relavent_reviews(user_query: str):
        """Retrieve information to help answer a query."""
        reviews = retriever.invoke(user_query)
        return reviews
    lc_tools = [get_relavent_reviews]
    print("Langchain Tools:", lc_tools)


    tools = mcp_tools+lc_tools
    agent = create_agent(
        model="ollama:qwen3.5:0.8b",
        tools=tools,
        system_prompt=prompt
    )

    st.title("Simple Streamlit Chat App")

    prompt = st.text_input("Enter your question:", value="Are the pizzas good?")
    if st.button("Ask"):
        with st.spinner("Getting answer..."):
            message = {"role": "user", "messages": prompt}
            response_full = await agent.ainvoke(message)
            st.success("Response received!")
            for response in response_full.get('messages') :
                if response.type == "ai":
                    st.write(response.content)

if __name__ == "__main__":
    asyncio.run(main())