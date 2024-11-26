# Group 10

## 1. 답변을 어떻게 해야 하는지에 대한 prompt 설정

## 2. 질문과 함께 자료로 넣어 줄 csv 파일

## 3. 1, 2번의 자료들로 답변을 얻을 RAG 모델 설정
- 윤수용 : 프로토 타입 답변을 제공하는 RAG 모델 시연

## 4. 와이어 프레임 작성
1. 홈 화면 (Home Screen)
1.1. 상단 바 (Header Bar)
    로고: 챗봇 서비스나 브랜드의 로고.
    챗봇 이름: 챗봇의 이름을 표시하여 사용자에게 어떤 서비스인지 명확히 전달.
    설정 아이콘: 사용자 설정, 언어 변경, 알림 설정 등에 접근할 수 있는 버튼.
    검색 버튼: 사용자가 원하는 정보를 바로 찾을 수 있도록 돕는 검색 기능.
    사용자 프로필 아이콘: 사용자 계정 정보나 로그인 상태 표시.
1.2. 메인 대화 영역 (Main Chat Area)
    대화 창:
    사용자가 주고받은 메시지가 표시되는 스크롤 가능한 공간.
    메시지는 사용자의 메시지와 챗봇의 응답으로 구분되어 표시.
    타임스탬프: 각 메시지 옆에 전송 시간 표시 (선택 사항).
    사용자 메시지: 왼쪽에 사용자가 입력한 텍스트, 이미지, 파일 등의 메시지 표시.
    챗봇 메시지: 오른쪽에 챗봇이 응답하는 텍스트, 이미지, 카드 형식의 메시지 표시.
    텍스트, 이미지, 비디오, 버튼 등의 다양한 응답 형식 제공.
1.3. 입력 영역 (Input Area)
    텍스트 입력 필드: 사용자가 메시지를 입력할 수 있는 공간.
    음성 입력 버튼: 사용자가 음성으로 메시지를 입력할 수 있는 버튼.
    첨부 파일 버튼: 사진, 파일, 위치 등의 첨부가 가능하도록 하는 버튼.
    전송 버튼: 메시지를 전송하는 버튼 (일반적으로 종이비행기 아이콘).
    메시지 예시 버튼: 사용자가 자주 묻는 질문에 대해 빠르게 답변을 받을 수 있도록 하는 예시 버튼 (예: "날씨", "교통", "뉴스").

2. 대화 흐름 (Dialogue Flow)
    2.1. 대화 시작 시나리오 (Initial Conversation Flow)
    인사 메시지: 챗봇이 사용자에게 인사를 건넴 ("안녕하세요! 무엇을 도와드릴까요?").
    주요 메뉴/옵션 제공: 사용자가 선택할 수 있는 옵션을 버튼 형태로 제공 (예: "날씨 확인", "최근 뉴스 보기", "계산기").
    상호작용 방식:
    버튼을 클릭하거나, 사용자가 텍스트로 직접 질문을 입력할 수 있도록 유도.
    2.2. 단계별 대화 흐름 (Step-by-Step Interaction)
    단계 1: 사용자가 원하는 옵션을 선택.
    예: "날씨 확인"을 선택하거나 "서울 날씨 알려줘"라고 텍스트 입력.
    단계 2: 챗봇이 선택된 옵션에 맞는 정보를 제공.
    예: "서울의 오늘 날씨는 맑고 기온은 25도입니다."
    단계 3: 추가적인 옵션이나 질문을 제공.
    예: "다른 지역 날씨를 확인하시겠어요?", "다시 시작하기" 등.
    2.3. 다양한 대화 형태 (Flexible Dialogue Forms)
    버튼 응답: 사용자 선택을 유도하는 버튼 제공 (예: "네", "아니오", "다시 시도").
    자연어 응답: 사용자 입력에 따라 챗봇이 자연스러운 언어로 응답.
    확인 대화: 사용자의 입력을 확인하는 메시지 (예: "서울 날씨를 확인해도 될까요?").
    2.4. 예외 처리 대화 흐름 (Error Handling)
    알 수 없는 입력: 사용자가 이해할 수 없는 입력을 했을 때, 챗봇은 "죄송합니다, 이해할 수 없습니다. 다른 방법으로 질문해 주세요."라고 안내.
    실패 시나리오: 예를 들어 API 오류나 서비스 불가 시 "현재 서비스가 중단되었습니다. 잠시 후 다시 시도해주세요." 등의 안내 메시지 표시.

3. 사용자 상호작용 (User Interaction)
    3.1. 메시지 반응 시간 (Response Time)
    로딩 스피너: 챗봇이 응답하는 동안 로딩 아이콘이나 스피너 표시.
    응답 시간 안내: 응답을 받기까지 예상 시간을 알려주는 메시지 (선택 사항).
    3.2. 사용자 맞춤형 기능 (Personalized Features)
    사용자 이름 호출: 사용자가 로그인 상태일 경우, 챗봇이 "안녕하세요, [사용자 이름]님!"으로 인사.
    위치 기반 서비스: 사용자의 위치 정보를 기반으로 날씨, 교통 등의 맞춤형 정보를 제공.
    사용자 학습: 사용자의 이전 대화 이력을 바탕으로 점차 개선된 대화 제공.

4. 기능별 화면 (Feature-specific Screens)
    4.1. 날씨 확인 화면
    날씨 정보 카드: 오늘의 날씨, 기온, 습도, 바람 속도 등을 카드 형식으로 제공.
    주간 날씨 예보: 주간 날씨 예보를 스와이프하여 확인할 수 있는 화면.
    다른 도시 날씨: 다른 도시의 날씨를 확인할 수 있는 선택 옵션 제공.
    4.2. 뉴스 확인 화면
    뉴스 카드: 최신 뉴스 기사를 카드 형식으로 제공.
    카테고리 선택: 정치, 경제, 스포츠 등 카테고리를 선택할 수 있는 기능.
    기사 공유 버튼: 사용자가 기사나 정보를 다른 사람과 공유할 수 있는 버튼.
    4.3. 계산기 화면
    계산기 인터페이스: 숫자 입력과 계산을 위한 간단한 인터페이스 제공.
    계산 결과: 계산 결과를 실시간으로 화면에 표시.

5. 설정 화면 (Settings Screen)
    5.1. 언어 설정
    언어 선택 버튼: 다국어 지원을 위해 다양한 언어를 선택할 수 있는 옵션 제공 (예: 한국어, 영어, 일본어 등).
    5.2. 알림 설정
    알림 스위치: 사용자가 알림을 켜거나 끌 수 있는 토글 스위치.
    알림 유형: 알림의 유형(예: 새로운 메시지 알림, 이벤트 알림 등) 선택.
    5.3. 개인 정보 설정
    사용자 프로필: 사용자가 이름, 이메일 등을 수정할 수 있는 화면.
    로그아웃: 사용자가 로그아웃할 수 있는 버튼.

6. 피드백 및 평가 (Feedback and Rating)
    피드백 요청: 대화가 끝난 후, 챗봇이 사용자에게 피드백을 요청 ("챗봇 사용에 대한 피드백을 남겨주세요").
    평점 시스템: 별점으로 서비스 만족도를 평가할 수 있는 시스템.
    피드백 수집: 사용자가 피드백을 남기거나 제안 사항을 입력할 수 있는 공간.

7. 시스템 및 오류 처리 (System and Error Handling)
    7.1. 서비스 불가 화면
    서비스 점검: "현재 서비스 점검 중입니다. 잠시 후 다시 시도해주세요." 등의 메시지.
    7.2. 네트워크 오류
    네트워크 문제: 네트워크 연결 문제 시 "인터넷 연결이 불안정합니다. 다시 시도해주세요." 메시지 표시.