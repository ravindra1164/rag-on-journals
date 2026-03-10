import streamlit as st
from openai import OpenAI

client = OpenAI(base_url="http://model-runner.docker.internal/engines/v1/", api_key="Loltestlol")

st.title("Simple Streamlit Chat App")

prompt = st.text_input("Enter your question:", value="What is the capital of France?")
if st.button("Ask"):
    with st.spinner("Getting answer..."):
        messages = [{"role": "user", "content": prompt}]
        try:
            response = client.chat.completions.create(
                model="ai/smollm2:135M-Q4_K_M",
                messages=messages,
            )
            st.success("Response received!")
            st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Error: {e}")