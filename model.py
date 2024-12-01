"""
LangChain Agent 이해하기 🤖
1. Agent란 무엇인가요?
Agent는 주어진 질문이나 작업을 해결하기 위해 다양한 도구(Tools)를 사용할 수 있는 '지능형 비서'라고 생각하면 됩니다. 마치 우리가 계산이 필요할 때 계산기를 사용하고, 정보가 필요할 때 인터넷을 검색하는 것처럼, Agent도 필요한 도구를 선택하고 사용하여 문제를 해결합니다.

2. Agent의 주요 구성 요소 📦
2.1 도구 (Tools)
정의: Agent가 사용할 수 있는 다양한 기능들
예시:
Calculator: 수학 계산을 수행
Wikipedia: 정보 검색을 수행
그 외: 날씨 확인, 일정 관리, 이메일 전송 등
2.2 LLM (Large Language Model)
역할: Agent의 '두뇌'
기능:
질문 이해
적절한 도구 선택
결과 해석 및 답변 생성
2.3 프롬프트 템플릿
역할: Agent의 '행동 지침서'
내용:
사용 가능한 도구 목록
도구 사용 규칙
답변 형식
3. Agent의 작동 프로세스 🔄
3.1 기본 실행 사이클
질문 → 도구 선택 → 도구 사용 → 결과 확인 → 최종 답변
3.2 상세 프로세스 예시
질문: "127*4 - 99는 얼마인가요?"

질문 분석 📝

"이것은 수학 계산이 필요한 질문이군요!"
도구 선택 🛠

Action: Calculator
Action Input: 127*4 - 99
도구 실행 및 관찰 👀

Observation: 409
최종 답변 생성 ✍️

Final Answer: 계산 결과는 409입니다.
"""

import streamlit as st
import pandas as pd
from langchain_experimental.agents import create_csv_agent
from langchain_community.llms import OpenAI
from langchain.tools import Tool
from langchain_community.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# OpenAI API Key 설정
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Streamlit에서 파일 업로드
st.title("Multiple CSV Agent")
uploaded_files = st.file_uploader("CSV 파일들을 업로드하세요", type=["csv"], accept_multiple_files=True)

if uploaded_files:
    # 모든 CSV 파일을 데이터프레임으로 로드
    dataframes = {}
    files_path = []  # csv 파일 경로
    for uploaded_file in uploaded_files:
        df = pd.read_csv(uploaded_file, on_bad_lines="skip")  # 열 크기가 맞지 않는 행은 무시
        dataframes[uploaded_file.name] = df  # 
        files_path.append(f"./files/jeju/{uploaded_file.name}")
        st.write(f"{uploaded_file.name} 데이터 미리보기:")
        st.dataframe(df)

    # 모든 CSV 데이터를 병합할 경우 (선택 사항)
    combined_df = pd.concat(dataframes.values(), ignore_index=True)

    # 사용자 질문 입력
    question = st.text_input("질문을 입력하세요:")

    if question:
        # LangChain Agent 생성
        tools = []
        for name, df in dataframes.items():
            # 각각의 CSV 파일을 하나의 Tool로 등록
            tool = Tool(
                name=name,
                func=lambda query, df=df: df.query(query),
                description=f" {name} 데이터셋을 분석하고, 결과를 한국어로 답변하세요."
            )
            tools.append(tool)

        # OpenAI LLM 초기화
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.1,
            streaming=True,
            openai_api_key = OPENAI_API_KEY,
        )

        # Agent 생성 및 질문 실행
        agent = create_csv_agent(
            llm=llm,  # 모델 지정
            path=files_path,  # csv 파일 경로들
            pandas_kwargs={"on_bad_lines":"skip"},  # 열 크기가 맞지 않는 행은 무시
            tools=tools,
            verbose=True,
            allow_dangerous_code=True,  # 보안 무시 (*로컬 컴퓨터에서만 실행!*)
        )
        response = agent.run(question)

        # 응답 출력
        st.write("AI 응답:")
        st.text(response)
