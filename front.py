import streamlit as st
import requests

# FastAPI 서버 URL
API_URL = "http://127.0.0.1:8000/ask"

# Streamlit UI 구성
st.title("Chat with GPT-4")
st.write("Type your question below and get a response.")

# 사용자 입력
user_input = st.text_input("Your Question:")

# 버튼 클릭 시 요청
if st.button("Send"):
    if user_input.strip():
        with st.spinner("Waiting for a response..."):
            # FastAPI 서버로 POST 요청
            response = requests.post(API_URL, json={"question": user_input})
            
            if response.status_code == 200:
                answer = response.json().get("answer", "No answer received.")
                st.write(f"**Answer:** {answer}")
            else:
                st.error("Failed to get a response from the server.")
    else:
        st.warning("Please enter a question.")