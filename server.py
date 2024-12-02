from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv, dotenv_values
from openai import OpenAI
import os

# OpenAI API 키 설정
#load_dotenv()
#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# config = dotenv_values('.env')
# OPENAI_API_KEY = config.get('OPENAI_API_KEY')

# OpenAI 초기화
# client = OpenAI(
#     api_key=None,
# )

# FastAPI 앱 초기화
app = FastAPI()

# 요청 모델 정의
class QueryRequest(BaseModel):
    api_key: str
    question: str

# 응답 생성 함수
def generate_response(api_key, question):   
    client = OpenAI(api_key=api_key)
    model = "gpt-4o"
    response = client.chat.completions.create(
        model=model,
        temperature=0.1,
        messages=[{"role":"user", "content":question}],
    )
    
    print(response)
    answer = response.choices[0].message.content
    return answer

# 엔드포인트 정의
@app.post("/ask")
async def ask_question(request: QueryRequest):
    api_key = request.api_key
    question = request.question
    answer = generate_response(api_key, question)
    return {"question": question, "answer": answer}

# 서버 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)