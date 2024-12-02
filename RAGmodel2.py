## LLM & RAG 전체적인 과정 ## 

# 1.라이브러리 설치
# pip install -r requirements.txt

# import os
# import json
# import pandas as pd
# import PyPDF2
# from sklearn.feature_extraction.text import TfidfVectorizer
# import faiss
# from langchain_community.llms import OpenAI
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain
# import streamlit as st

# # 1. OpenAI API 키 설정
# def set_openai_api_key():
#     """OpenAI API 키를 설정합니다."""
#     from getpass import getpass
#     os.environ["OPENAI_API_KEY"] = getpass("OpenAI API 키를 입력하세요:")

# set_openai_api_key()

# # 2. 파일 읽기
# def read_file_list(file_list_path):
#     """files.txt에서 파일 경로를 읽어옵니다."""
#     with open(file_list_path, "r", encoding="utf-8") as f:
#         return [line.strip() for line in f if line.strip()]

# def process_pdf(file_path):
#     """PDF 파일에서 텍스트를 추출합니다."""
#     try:
#         with open(file_path, 'rb') as file:
#             reader = PyPDF2.PdfReader(file)
#             text = ""
#             for page in reader.pages:
#                 text += page.extract_text()
#         return text
#     except Exception as e:
#         print(f"PDF 처리 중 오류 발생: {file_path} - {str(e)}")
#         return ""

# def process_csv(file_path):
#     """CSV 파일 데이터를 텍스트로 변환합니다."""
#     try:
#         df = pd.read_csv(file_path)
#         return df.to_string()
#     except Exception as e:
#         print(f"CSV 처리 중 오류 발생: {file_path} - {str(e)}")
#         return ""

# def chunk_text(text, chunk_size=500, overlap=50):
#     """텍스트를 청크로 분할합니다."""
#     chunks = []
#     start = 0
#     while start < len(text):
#         end = min(start + chunk_size, len(text))
#         chunks.append(text[start:end])
#         start += chunk_size - overlap
#     return chunks

# def process_and_chunk_files(file_list_path):
#     """파일을 처리하고 텍스트를 청크로 분할합니다."""
#     files = read_file_list(file_list_path)
#     combined_chunks = []

#     for file_path in files:
#         print(f"파일 처리 중: {file_path}")
#         if file_path.endswith(".pdf"):
#             text = process_pdf(file_path)
#             if text.strip():
#                 combined_chunks.extend(chunk_text(text))
#             else:
#                 print(f"PDF 파일에서 텍스트를 추출하지 못했습니다: {file_path}")
#         elif file_path.endswith(".csv"):
#             text = process_csv(file_path)
#             if text.strip():
#                 combined_chunks.extend(chunk_text(text))
#             else:
#                 print(f"CSV 파일에서 데이터를 추출하지 못했습니다: {file_path}")
#         else:
#             print(f"알 수 없는 파일 형식: {file_path}")

#     if not combined_chunks:
#         raise ValueError("모든 파일에서 텍스트를 추출하지 못했습니다. 파일 경로와 내용을 확인하세요.")
#     return combined_chunks

# # 3. FAISS 인덱스 생성
# def create_faiss_index(documents):
#     """텍스트 데이터를 벡터화하고 FAISS 인덱스를 생성합니다."""
#     if not documents:
#         raise ValueError("벡터화할 데이터가 없습니다. 텍스트 데이터를 확인하세요.")
#     vectorizer = TfidfVectorizer(stop_words=None)
#     vectors = vectorizer.fit_transform(documents)
#     index = faiss.IndexFlatL2(vectors.shape[1])
#     index.add(vectors.toarray().astype('float32'))
#     return vectorizer, index

# # 4. LangChain 질문-응답 체인 생성
# def create_rag_chain():
#     """LangChain 기반 AI 질문-응답 체인을 생성합니다."""
#     llm = OpenAI(model="gpt-4")  # langchain-community의 OpenAI
#     prompt = PromptTemplate(
#         input_variables=["context", "question"],
#         template="문맥: {context}\n\n질문: {question}\n\n답변:"
#     )
#     return LLMChain(llm=llm, prompt=prompt)

# # 5. 질문 실행 및 JSON 저장
# def answer_question_save_json(query, vectorizer, index, documents, rag_chain, output_path="output.json"):
#     """질문에 응답하고 결과를 JSON으로 저장합니다."""
#     query_vector = vectorizer.transform([query]).toarray().astype('float32')
#     distances, indices = index.search(query_vector, k=1)
#     relevant_doc = documents[indices[0][0]]
#     response = rag_chain.run({"context": relevant_doc, "question": query})

#     # 결과 저장
#     result = {
#         "query": query,
#         "context": relevant_doc,
#         "answer": response
#     }
#     with open(output_path, "w", encoding="utf-8") as f:
#         json.dump(result, f, ensure_ascii=False, indent=4)
#     return result

# # # 6. Streamlit 인터페이스 실행
# # def run_chatbot(file_list_path):
# #     """Streamlit을 사용해 AI 챗봇을 실행합니다."""
# #     st.title("RAG 기반 AI 챗봇")
# #     st.write("PDF와 CSV 파일에서 데이터를 읽고 AI가 질문에 답변합니다.")

# #     # 데이터 처리
# #     documents = process_and_chunk_files(file_list_path)
# #     vectorizer, index = create_faiss_index(documents)
# #     rag_chain = create_rag_chain()

# #     # 사용자 입력 처리
# #     user_query = st.text_input("질문을 입력하세요:")
# #     if user_query:
# #         result = answer_question_save_json(user_query, vectorizer, index, documents, rag_chain)
# #         st.write("**AI 응답:**")
# #         st.write(result["answer"])
# #         st.write("**관련 문맥:**")
# #         st.write(result["context"])

# #실행
# file_list_path = "files.txt"  # `files.txt` 파일에서 경로를 읽어옵니다.
# # run_chatbot(file_list_path)




import os
from sklearn.feature_extraction.text import TfidfVectorizer
import faiss
from PyPDF2 import PdfReader
import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain


# 1. OpenAI API 키 설정
os.environ["OPENAI_API_KEY"] = "API키"

# 2. 파일 처리 및 청크 분할 함수
def process_and_chunk_files(file_list_path):
    """파일 목록을 읽고 각 파일의 텍스트를 추출한 뒤 청크로 분할합니다."""
    # 파일 목록 읽기
    with open(file_list_path, 'r', encoding='utf-8') as file:
        file_paths = [line.strip() for line in file]

    documents = []

    for file_path in file_paths:
        if file_path.endswith('.pdf'):
            # PDF 파일 처리
            try:
                text = ""
                with open(file_path, 'rb') as f:
                    reader = PdfReader(f)
                    for page in reader.pages:
                        text += page.extract_text()
                documents.extend(chunk_text(text))
            except Exception as e:
                print(f"PDF 파일 처리 중 오류 발생: {file_path}, 오류: {e}")

        elif file_path.endswith('.csv'):
            # CSV 파일 처리
            try:
                df = pd.read_csv(file_path)
                text = "\n".join(df.astype(str).apply(" ".join, axis=1))
                documents.extend(chunk_text(text))
            except Exception as e:
                print(f"CSV 파일 처리 중 오류 발생: {file_path}, 오류: {e}")

        else:
            print(f"지원하지 않는 파일 형식: {file_path}")

    if not documents:
        raise ValueError("파일에서 데이터를 추출하지 못했습니다. 파일 내용을 확인하세요.")

    return documents

def chunk_text(text, chunk_size=500, overlap=50):
    """텍스트를 일정 크기로 청크 분할."""
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


# 3. FAISS 인덱스 생성 함수
def create_faiss_index(documents):
    """텍스트 데이터를 벡터화하고 FAISS 인덱스를 생성합니다."""
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(documents)
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors.toarray().astype('float32'))
    return vectorizer, index


# 4. LangChain 질문-응답 체인 생성 함수
def create_rag_chain():
    """LangChain 기반 AI 질문-응답 체인을 생성합니다."""
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.7
    )

    # 프롬프트 템플릿
    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 한국어로 답변하는 AI 비서입니다. 제주도 창업 사업기획서 관련 질문에 정확하고 자세히 답변합니다."),
        HumanMessagePromptTemplate.from_template(
            "문맥: {context}\n\n질문: {question}\n\n답변을 한글로 작성해주세요. 구체적이고 체계적으로 작성해주세요."
        )
    ])

    return LLMChain(llm=llm, prompt=prompt)


# 5. 질문-응답 처리 함수
def generate_response(vectorizer, index, documents, query, rag_chain):
    """질문을 처리하고 관련 문서에서 답변을 생성합니다."""
    query_vector = vectorizer.transform([query]).toarray().astype('float32')
    distances, indices = index.search(query_vector, k=1)

    # 검색된 문서 가져오기
    if indices[0][0] < len(documents) and distances[0][0] != float("inf"):
        relevant_doc = documents[indices[0][0]]
    else:
        relevant_doc = None

    if relevant_doc:
        print(f"\n선택된 문맥:\n{relevant_doc}")
        try:
            response = rag_chain.run({"context": relevant_doc, "question": query})
            return response
        except Exception as e:
            return f"답변 생성 중 오류 발생: {e}"
    else:
        return "관련 문서를 찾을 수 없습니다."


# 6. 터미널에서 질문-응답 처리 함수
def terminal_chatbot(file_list_path):
    """터미널에서 질문-응답을 처리하는 챗봇."""
    print("=== RAG 기반 터미널 챗봇 ===")
    print("파일 목록을 처리하고 AI 모델을 초기화 중입니다...")

    # 데이터 처리 및 인덱스 생성
    documents = process_and_chunk_files(file_list_path)
    vectorizer, index = create_faiss_index(documents)
    rag_chain = create_rag_chain()

    print(f"총 {len(documents)}개의 문서가 처리되었습니다.")
    print("질문을 입력하세요 (종료하려면 'exit' 입력):")

    while True:
        query = input("\n> 질문: ")
        if query.lower() == "exit":
            print("챗봇을 종료합니다.")
            break

        # 답변 생성
        response = generate_response(vectorizer, index, documents, query, rag_chain)
        print(f"\nAI 답변:\n{response}")


# 7. 실행 블록
if __name__ == "__main__":
    file_list_path = "files.txt"  # 파일 경로가 저장된 텍스트 파일
    terminal_chatbot(file_list_path)

# ===== 프롬프트 예시 =====
"""
1. 창업 아이템을 개발하는 방법은?
2. 제주도에서 창업 아이템의 타겟 시장은 무엇인가요?
3. 제주도의 창업 지원 정책은 어떤 것이 있나요?
4. 창업 초기 자금 조달 방법은 무엇인가요?
5. 시장 분석 및 경쟁사 분석 방법은?
6. 고객의 니즈를 조사하는 방법은 무엇인가요?
7. 창업 성공을 위한 필수 요인은 무엇인가요?
8. 팀 구성과 역할 분배를 어떻게 해야 하나요?
9. 기술 창업의 장점과 단점은 무엇인가요?
10. 지속 가능한 비즈니스 모델을 설계하려면 어떻게 해야 하나요?
11. 친환경 창업 아이템 개발 방안은?
12. 창업 아이템의 차별화 전략은 무엇인가요?
13. 제주도의 관광 자원을 활용한 창업 아이템은 무엇인가요?
14. 고객을 확보하는 전략은 무엇인가요?
15. 초기 창업 아이템의 MVP(최소 기능 제품)를 설계하려면 어떻게 해야 하나요?
16. 창업 자금의 사용 계획을 어떻게 작성하나요?
17. 창업의 법적 요건과 허가 절차는 무엇인가요?
18. 글로벌 시장으로 진출하려면 어떤 전략이 필요한가요?
19. 창업 후 성공 사례를 분석해보세요.
20. 실패하지 않는 창업의 비법은 무엇인가요?
"""

