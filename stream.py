import streamlit as st
import sqlite3
from datetime import datetime
from openai import OpenAI
import re
import uuid

class ChatHistoryManager:
    def __init__(self, db_path='chat_history.db'):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    role TEXT,
                    content TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def add_message(self, role, content, session_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)',
                (session_id, role, content)
            )
            conn.commit()

    def get_messages(self, session_id, limit=50):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT role, content, timestamp FROM messages WHERE session_id = ? ORDER BY timestamp DESC LIMIT ?',
                (session_id, limit)
            )
            return cursor.fetchall()

    def search_messages(self, query, session_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT role, content, timestamp FROM messages WHERE session_id = ? AND content LIKE ? ORDER BY timestamp DESC',
                (session_id, f'%{query}%')
            )
            return cursor.fetchall()

    def clear_history(self, session_id=None):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if session_id:
                cursor.execute('DELETE FROM messages WHERE session_id = ?', (session_id,))
            else:
                cursor.execute('DELETE FROM messages')
            conn.commit()

def generate_ai_response(client, messages, history_manager):
    try:
        context_messages = [
            {"role": "system", "content": "You are an expert advisor for startup businesses in Jeju Island."}
        ]
        context_messages.extend([
            {"role": msg["role"], "content": msg["content"]} for msg in messages[-10:]
        ])
        full_response = ""
        message_placeholder = st.empty()
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=context_messages,
            stream=True
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        return full_response
    except Exception as e:
        st.error(f"AI 응답 생성 중 오류 발생: {e}")
        return None

def show_intro():
    with st.expander("📖 제주 창업 계획 도우미 사용 가이드 (펼쳐보기)"):
        st.markdown("""
        ### 🏝️ 제주 창업 계획 도우미 사용 안내
        이 앱은 제주도 창업을 준비하는 분들을 위한 맞춤형 지원 도구입니다. 아래 기능들을 활용하여 효과적으로 질문하고 필요한 정보를 찾아보세요!

        #### 주요 기능
        1. **채팅**
           - 창업 관련 질문을 입력하거나, AI와 자유롭게 대화할 수 있습니다.
           - 질문에 대한 AI 응답을 실시간으로 확인하세요.
        2. **채팅 히스토리**
           - 이전에 나눴던 대화를 확인할 수 있습니다.
           - 최대 100개의 최근 대화 내용을 표시합니다.
        3. **히스토리 검색**
           - 특정 키워드로 과거 대화를 검색할 수 있습니다.
           - 검색된 메시지에서 키워드가 하이라이트 처리되어 표시됩니다.
        4. **대화 초기화**
           - 현재 대화를 초기화하여 새로운 대화를 시작할 수 있습니다.
           - 초기화 시, 이전 대화는 삭제되지 않고 기록에 남습니다.
        5. **히스토리 초기화**
           - 모든 채팅 히스토리를 삭제하여 기록을 완전히 지울 수 있습니다.
           - 주의: 삭제된 히스토리는 복구할 수 없습니다.
        6. **빠른 질문**
           - AI가 자주 묻는 질문에 대해 바로 응답할 수 있는 옵션을 제공합니다.
           - 예: "제주 지역 창업 아이템 추천", "정부 지원 및 자금 확보 방법" 등.

        #### 시작하기
        - **1단계**: 좌측 사이드바에서 OpenAI API 키를 입력하세요.
        - **2단계**: 원하는 메뉴(채팅, 히스토리 등)를 선택하여 이용하세요.
        - **Tip**: 사이드바의 빠른 질문 버튼을 사용하면 더 쉽게 시작할 수 있습니다!

        #### 자주 묻는 질문
        - **API 키가 없어요!**
          - OpenAI의 [공식 웹사이트](https://openai.com/)에서 API 키를 발급받으세요.
        - **AI 응답이 느리게 표시됩니다.**
          - 응답은 스트리밍 방식으로 제공됩니다. 잠시 기다려 주세요!

        #### 🌟 문의 및 개선사항
        - 더 좋은 사용자 경험을 위해 피드백을 언제든 환영합니다!
        - 문의 : mamemimomu0820@gmail.com
        """)

def main():
    st.set_page_config(page_title="제주도 창업 계획", page_icon="🏝️")
    st.title("🏝️ 제주도 창업 계획 도우미")
    st.subheader("안녕하세요!! 성공적인 제주 창업을 도와주는 사업 계획 도우미입니다. 무엇을 알려드릴까요?")

    show_intro()

    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    session_id = st.session_state.session_id

    history_manager = ChatHistoryManager()

    st.sidebar.header("🔑 OpenAI API Key")
    api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
    client = OpenAI(api_key=api_key) if api_key else None

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    if st.sidebar.button("대화 초기화"):
        st.session_state.messages = []
        st.rerun()

    menu = st.sidebar.radio("메뉴", ["채팅", "채팅 히스토리", "히스토리 검색"])

    if menu == "채팅":
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if client:
            st.sidebar.header("🚀 빠른 질문")
            quick_questions = [
                "제주 지역 창업 아이템 추천",
                "정부 지원 및 자금 확보",
                "법적/행정적 필수 절차"
            ]
            for question in quick_questions:
                if st.sidebar.button(question):
                    st.session_state.messages.append({"role": "user", "content": question})
                    with st.chat_message("user"):
                        st.markdown(question)
                    history_manager.add_message("user", question, session_id)
                    with st.chat_message("assistant"):
                        full_response = generate_ai_response(client, st.session_state.messages, history_manager)
                        if full_response:
                            st.session_state.messages.append({"role": "assistant", "content": full_response})
                            history_manager.add_message("assistant", full_response, session_id)

            if prompt := st.chat_input("창업 아이디어 또는 질문을 입력하세요"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)
                history_manager.add_message("user", prompt, session_id)
                with st.chat_message("assistant"):
                    full_response = generate_ai_response(client, st.session_state.messages, history_manager)
                    if full_response:
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                        history_manager.add_message("assistant", full_response, session_id)
        else:
            st.warning("OpenAI API 키를 입력해주세요.")

    elif menu == "채팅 히스토리":
        st.header("📜 채팅 히스토리")
        messages = history_manager.get_messages(session_id, limit=100)
        for msg in messages:
            role, content, timestamp = msg
            formatted_timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M")
            if role == "user":
                st.markdown(f"**👤 사용자 [{formatted_timestamp}]:**\n{content}")
            else:
                st.markdown(f"**🤖 AI [{formatted_timestamp}]:**\n{content}")
            st.divider()

        if st.button("전체 히스토리 삭제"):
            history_manager.clear_history(session_id)
            st.success("채팅 히스토리가 삭제되었습니다.")

    elif menu == "히스토리 검색":
        st.header("🔍 히스토리 검색")
        search_query = st.text_input("검색어를 입력하세요")
        if search_query:
            results = history_manager.search_messages(search_query, session_id)
            st.subheader(f"'{search_query}' 검색 결과")
            if results:
                for msg in results:
                    role, content, timestamp = msg
                    formatted_timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M")
                    highlighted_content = re.sub(
                        f'({re.escape(search_query)})',
                        r'**\1**',
                        content,
                        flags=re.IGNORECASE
                    )
                    if role == "user":
                        st.markdown(f"**👤 사용자 [{formatted_timestamp}]:**\n{highlighted_content}")
                    else:
                        st.markdown(f"**🤖 AI [{formatted_timestamp}]:**\n{highlighted_content}")
                    st.divider()
            else:
                st.info("검색 결과가 없습니다.")

if __name__ == "__main__":
    main()