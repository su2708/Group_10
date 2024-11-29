import streamlit as st
import sqlite3
from datetime import datetime
from openai import OpenAI
import re

class ChatHistoryManager:
    def __init__(self, db_path='chat_history.db'):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """데이터베이스 초기화 및 테이블 생성"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT,
                    content TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def add_message(self, role, content):
        """메시지 추가"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO messages (role, content) VALUES (?, ?)', 
                (role, content)
            )
            conn.commit()

    def get_messages(self, limit=50):
        """최근 메시지 가져오기"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT role, content, timestamp FROM messages ORDER BY timestamp DESC LIMIT ?', 
                (limit,)
            )
            return cursor.fetchall()

    def search_messages(self, query):
        """메시지 검색"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT role, content, timestamp FROM messages WHERE content LIKE ? ORDER BY timestamp DESC', 
                (f'%{query}%',)
            )
            return cursor.fetchall()

    def clear_history(self):
        """전체 채팅 히스토리 삭제"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM messages')
            conn.commit()

def main():
    # 페이지 설정
    st.set_page_config(page_title="제주도 창업 계획", page_icon="🏝️")
    st.title("🏝️ 제주도 창업 계획 도우미")
    st.subheader("안녕하세요!! 성공적인 제주 창업을 도와주는 사업 계획 도우미입니다. 무엇을 알려드릴까요?")

    # 세션 상태 초기화
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # 히스토리 관리자 초기화
    history_manager = ChatHistoryManager()

    # OpenAI 클라이언트 초기화
    st.sidebar.header("🔑 OpenAI API Key")
    api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
    client = OpenAI(api_key=api_key) if api_key else None

    # 사이드바 메뉴
    menu = st.sidebar.radio("메뉴", ["채팅", "채팅 히스토리", "히스토리 검색"])

    if menu == "채팅":
        # 기존 메시지 표시
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # 채팅 인터페이스
        if client:
            # 채팅 입력란
            if prompt := st.chat_input("창업 아이디어 또는 질문을 입력하세요"):
                # 사용자 메시지 저장 및 표시
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)
                history_manager.add_message("user", prompt)

                # AI 응답 생성
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    full_response = ""
                    
                    try:
                        # 최근 메시지 컨텍스트로 사용
                        context_messages = [
                            {"role": msg["role"], "content": msg["content"]} 
                            for msg in st.session_state.messages[-10:]
                        ]
                        
                        # 응답 스트리밍
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
                        
                        # AI 응답 저장
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                        history_manager.add_message("assistant", full_response)
                    
                    except Exception as e:
                        st.error(f"오류 발생: {e}")

        else:
            st.warning("OpenAI API 키를 입력해주세요.")

        # 대화 초기화 버튼
        if st.sidebar.button("대화 초기화"):
            st.session_state.messages = []
            st.rerun()

    elif menu == "채팅 히스토리":
        st.header("📜 채팅 히스토리")
        
        # 최근 메시지 표시
        messages = history_manager.get_messages(limit=100)
        
        for msg in messages:
            role, content, timestamp = msg
            formatted_timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M")
            
            if role == "user":
                st.markdown(f"**👤 사용자 [{formatted_timestamp}]:**\n{content}")
            else:
                st.markdown(f"**🤖 AI [{formatted_timestamp}]:**\n{content}")
            
            st.divider()
        
        # 히스토리 삭제 버튼
        if st.button("전체 히스토리 삭제"):
            history_manager.clear_history()
            st.success("채팅 히스토리가 삭제되었습니다.")

    elif menu == "히스토리 검색":
        st.header("🔍 히스토리 검색")
        
        # 검색 입력란
        search_query = st.text_input("검색어를 입력하세요")
        
        if search_query:
            # 검색 결과 표시
            results = history_manager.search_messages(search_query)
            
            st.subheader(f"'{search_query}' 검색 결과")
            
            if results:
                for msg in results:
                    role, content, timestamp = msg
                    formatted_timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M")
                    
                    # 검색어 하이라이트
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