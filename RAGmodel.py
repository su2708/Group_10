## LLM & RAG 전체적인 과정 ## 

# 1.라이브러리 설치
# pip install -r requirements.txt

#OpenAI API 키 설정
import os
from getpass import getpass

# OpenAI API 키 입력 받기
os.environ["OPENAI_API_KEY"] = getpass("OpenAI API 키를 입력하세요:")


# 2.PDF파일 데이터 읽기
import PyPDF2

# PDF 파일 경로 설정
#pdf파일 경로설정
pdf_file_path = r"C:[별첨 3] 창업사업화 지원사업 사업계획서 작성 가이드 (1).pdf"  

# PDF 파일 열기
with open(pdf_file_path, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    text = ""
    # 각 페이지에서 텍스트 추출
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()

# 추출된 텍스트 출력
print(text)



# 3. csv파일 읽기
import pandas as pd

# CSV 파일 경로 설정
 #csv파일 경로 설정
csv_file_path = r"C:\성별카드이용금액비율.csv"
# file_path_1 = r"C:\성별카드이용금액비율.csv"
# file_path_2 = r"C:\시간대별카드이용금액현황.csv"
# file_path_3 = r"C:\요일별카드이용건수비교.csv"

# CSV 파일 읽기
df = pd.read_csv(csv_file_path)

# CSV 데이터의 첫 5행 출력
print(df.head())

# 필요한 열 추출 (예시: 'text' 열이 있다고 가정)
texts_from_csv = df['text'].tolist()

# 출력 예시
print(texts_from_csv)


#4. 텍스트 벡터화
from sklearn.feature_extraction.text import TfidfVectorizer

# PDF와 CSV에서 추출한 텍스트 데이터를 합침
documents = [text] + texts_from_csv  # 텍스트 리스트 (PDF 텍스트 + CSV 텍스트)

# TF-IDF 벡터화기
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(documents)

# 벡터화된 데이터 확인
print(X.toarray())


# 5. FAISS로 벡터 저장 및 검색
import faiss
import numpy as np

# FAISS 인덱스 생성
index = faiss.IndexFlatL2(X.shape[1])  # L2 거리 계산

# 데이터를 FAISS 인덱스에 추가
index.add(np.array(X.toarray(), dtype=np.float32))

# 쿼리 텍스트
query = ["What is the first document about?"]
query_vec = vectorizer.transform(query).toarray()

# FAISS로 가장 가까운 벡터 검색
D, I = index.search(np.array(query_vec, dtype=np.float32), k=1)

# 결과 출력
print("가장 관련성 높은 문서 인덱스:", I)
print("가장 관련성 높은 문서의 거리:", D)


#6.langchain RAG 모델 설정
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.vectorstores import FAISS

# FAISS로 검색된 결과를 LangChain에 연결
faiss_index = FAISS.from_documents(documents, embedding=vectorizer)

# OpenAI 모델 설정
llm = OpenAI(model="gpt-3.5-turbo")

# 프롬프트 템플릿 설정 (사용자의 질문과 문맥)
contextual_prompt = PromptTemplate.from_messages([
    ("system", "다음 문맥을 바탕으로 질문에 답해 주세요."),
    ("user", "문맥: {context}\n질문: {question}")
])

# 예시부분 프롬프트 추가할 사항 여기에 예시로 추가
# example_question = "xxxxxxxxxxxxxxxxxxxxx?"
# example_question = "xxxxxxxxxxxxxxxxxxxxx?"
# example_question = "xxxxxxxxxxxxxxxxxxxxx?"
# example_question = "xxxxxxxxxxxxxxxxxxxxx?"
# examole_context = "xxxxxxxxxxx xxxxxx xxxxx."

#프롬프트 생성 코드
#formatted_prompt = contextual_prompt.format_messages(context=example_context, question=example_question)
#프롬프트 출력
#print(formatted_prompt)

# LangChain을 통한 질문 응답 체인 설정
rag_chain = LLMChain(llm=llm, prompt=contextual_prompt)

# 쿼리를 기반으로 RAG 시스템 실행
query = "이 문서에서 GPT 모델의 활용 사례를 설명해 주세요."
response = rag_chain.run({"context": documents[I[0][0]], "question": query})
print(response)

# 7.json형식 출력 추가 출력방식
import json

# JSON 형식으로 출력
output = {
    "query": query,
    "answer": response
}

# JSON 형식으로 출력
print(json.dumps(output, ensure_ascii=False, indent=4))

