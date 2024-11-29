import os
import pandas as pd
from langchain_unstructured.document_loaders import UnstructuredLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema.runnable import RunnablePassthrough
from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables.base import RunnableMap
from dotenv import load_dotenv

# 1. CSV 파일을 TXT로 변환
def csv_to_txt(csv_files, txt_file):
    with open(txt_file, "w", encoding="utf-8") as f:
        for file in csv_files:
            df = pd.read_csv(file, on_bad_lines="skip")
            count = 0
            for _, row in df.iterrows():
                # 모든 열의 데이터를 문자열로 병합
                row_text = " | ".join([f"{col}: {str(row[col])}" for col in df.columns])
                f.write(f"{row_text}\n")
                count += 1
                if count > 10:
                    break
                else:
                    continue
    print(f"CSV 파일들이 '{txt_file}'로 변환되었습니다.")

# 2. TXT 파일을 Document 객체로 변환
def txt_to_documents(txt_file):
    loader = UnstructuredLoader(file_path=txt_file)
    return loader.load()

# 3. 문서를 Chunk로 분할
def split_documents(documents, chunk_size=512, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(documents)

# 4. 문서 임베딩 및 벡터스토어 생성
def create_vectorstore(documents, embeddings_model="text-embedding-ada-002"):
    embeddings = OpenAIEmbeddings(model=embeddings_model)
    vectorstore = FAISS.from_documents(documents, embeddings)
    return vectorstore

# 5. Few-shot Prompt Template 정의
def define_prompt_template():
    examples = [
        {"query": "현대적인 웹 프레임워크란?", "answer": "FastAPI는 현대적인 웹 프레임워크입니다."},
        {"query": "RAG 모델이란 무엇인가요?", "answer": "RAG 모델은 검색과 생성을 결합한 기술입니다."},
    ]
    
    example_str = "\n".join([f"질문: {e['query']} / 답변: {e['answer']}" for e in examples])
    
    template = """
    당신은 질문에 정확하고 간결하게 답변하는 전문가입니다. 
    다음은 몇 가지 예시입니다:

    {examples}

    질문: {query}
    답변:
    """
    return example_str, template

# 6. RAG 모델 체인 생성 (LangChain Execution Chain Language 사용)
def create_rag_chain(vectorstore, prompt_template):
    retriever = vectorstore.as_retriever()
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.1,
        api_key = OPENAI_API_KEY,
    )
    # chain = RetrievalQA.from_chain_type(
    #     llm=llm,
    #     retriever=retriever,
    #     return_source_documents=True,
    #     chain_type_kwargs={"prompt": prompt_template}
    # )
    
    #return chain
    pass

# 실행 코드
if __name__ == "__main__":
    # OpenAI API 키 설정
    load_dotenv()
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # CSV 파일 설정
    csv_files = []
    base_dir = "./files/jeju"
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            file_path = os.path.join(root, file)
            csv_files.append(file_path)
    txt_file = "combined.txt"

    # 1. CSV → TXT 변환
    csv_to_txt(csv_files, txt_file)

    # 2. TXT → Document 변환
    documents = txt_to_documents(txt_file)

    # 3. Document Split
    split_docs = split_documents(documents)

    # 4. Vectorstore 생성
    vectorstore = create_vectorstore(split_docs)

    # 5. Prompt Template 정의
    example_str, template = define_prompt_template()
    prompt = PromptTemplate.from_template(template)

    # 6. RAG Chain 생성
    #rag_chain = create_rag_chain(vectorstore, prompt_template)
    retriever = vectorstore.as_retriever()
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.1,
        api_key = OPENAI_API_KEY,
    )
    
    # RAG 체인 생성
    rag_chain = (
        RunnableMap({"query": RunnablePassthrough()})  # query만 retriever로 전달
        | retriever  # retriever에서 query 처리 및 문서 검색
        | RunnableMap({
            "examples": lambda inputs: example_str,  # examples 추가
            "query": lambda inputs: inputs["query"],  # query 유지
            "context": lambda inputs: "\n".join([doc.page_content for doc in inputs]),  # 검색된 문서를 context로 변환
        })
        | prompt  # 프롬프트 생성
        | llm  # 응답 생성
    )
    
    # 7. 질문 예제 테스트
    query = "현대적인 웹 프레임워크란 무엇인가요?"
    response = rag_chain.invoke({"example": example_str, "query": query})

    print("질문:", query)
    print("응답:", response)
