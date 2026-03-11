import streamlit as st
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

model = OllamaLLM(model="smollm2:135m")
template = """
You are an exeprt in answering questions about a pizza restaurant

Here are some relevant reviews: {reviews}

Here is the question to answer: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

st.title("Simple Streamlit Chat App")

prompt = st.text_input("Enter your question:", value="What is the capital of France?")
if st.button("Ask"):
    with st.spinner("Getting answer..."):
        messages = [{"role": "user", "content": prompt}]
        reviews = retriever.invoke(prompt)
        result = chain.invoke({"reviews": reviews, "question": prompt})
        st.success("Response received!")
        st.write(result)
        