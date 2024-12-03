# Group 10

# **창업 사업 기획서 챗봇 (사업아이템 및 투자전략 지원)**

---

## 📌 프로젝트 소개  
**창업 아이디어 및 사업계획서 작성 과정을 지원하는 AI 기반 챗봇**입니다.  
사용자가 입력한 데이터를 기반으로 투자 전략, 시장 분석, 고객 페르소나 등 사업계획서 작성의 핵심 섹션을 자동화합니다.  

---

## 🎯 프로젝트 핵심 목표  

1. **창업 과정의 효율성 향상**  
   - 사업계획서 작성 및 분석 과정을 자동화하여 시간과 비용 절감  
2. **사용자 중심의 대화형 인터페이스 제공**  
   - 창업 아이디어, 타겟 고객, 시장 분석 등 대화형으로 필요한 정보를 제공  
3. **결과물 저장 및 활용 기능 강화**  
   - 생성된 분석 데이터를 텍스트(CSV, PDF) 파일로 다운로드 가능

---

## 🌟 Key Summary  

### ✅ **가장 돋보이는 성과**  
1. **Streamlit 기반 UI 설계**: 사용자 친화적인 인터페이스 제공
2. **FastAPI와 LLM 통합**: 실시간으로 창업 아이디어에 대해 맞춤형 분석 결과를 제공 
3. **임베딩 기반 데이터 검색**: 대규모 창업 데이터를 효율적으로 활용한 결과 생성 

---

## 🏗️ 인프라 아키텍처 & 적용 기술  

## 시스템 개요

![시스템 개요 다이어그램](images/시스템개요.png)

---

## ⚙️ 주요 기능

1. **대화형 인터페이스**
    - 사용자가 창업 아이디어를 입력하면 실시간으로 피드백 제공.
    - **예시 질문**:
      - "고객 타겟팅을 어떻게 설정하면 좋을까?"
      - "내 시장 규모를 분석해줘"

2. **섹션별 결과 생성**
    - 고객 현황 분석, 시장 규모 평가 등 창업에 필요한 주요 데이터를 분석

---

## 🛠️ 기술적 고도화

<details>
<summary><strong>[성과 및 기술적 깊이: 고객 페르소나 분석]<strong></summary>

### **[구현한 기능]**
- 고객 데이터를 분석하고 타겟 고객의 특징을 도출하는 기능

### **[주요 로직]**
- LangChain 기반의 LLM과 데이터 임베딩 기술을 사용하여 입력된 데이터를 분석
- 데이터를 토큰화하고 주요 패턴을 시각화하여 사용자에게 제공

### **[배경 및 요구사항]**
1. **배경**: 창업 초기 단계에서 타겟 고객을 명확히 설정하는 것이 성공의 핵심
2. **요구사항**: 입력 데이터를 분석하여 연령, 관심사, 주요 니즈 등의 고객들을 파악

### **[의사결정 및 성과]**
- **기술 도입**: Langchain을 사용하여 빠르고 정확한 데이터 처리
- **결과**: 고객 맞춤 텍스트가 생성 정확도가 개선됨

</details>

<details>
<summary><strong>[성과 및 기술적 깊이: 시장 규모 분석]<strong></summary>

### **[문제 정의]**
- 시장 규모를 추정할 때 데이터를 체계적으로 정리하고 제공하는 기능이 부족

### **[해결 과정]**
1. **임베딩 기반 데이터 검색**: 관련 데이터베이스에서 정확한 시장 데이터를 추출.
2. **FastAPI와 통합**: 실시간 응답 속도를 유지하면서 대량 데이터를 처리

### **[결과]**
- 분석 결과 응답 시간 단축
- 시장 규모 추정 정확도 상승

</details>

---

## 🤝 역할 분담 및 협업 방식

| 역할          | 담당자         | 주요 업무                              |
|---------------|---------------|---------------------------------------|
| **팀장**      | 윤수용         | 자료 크롤링, FastAPI 설계 및 시스템 통합 |
| **데이터 처리** | 이형민, 정석훈 | 자료 임베딩, 데이터 전처리, RAG 모델 설계 |
| **UI 개발**    | 이지훈         | Streamlit UI 설계, 발표자료 제작        |

---

## 📈 성과 및 회고

### **성과**
1. 창업 관련 챗봇으로서 데이터 기반 분석 결과 제공.
2. 시장 분석 및 고객 분석 기능으로 **사용자 신뢰도 향상**

### **회고 및 향후 계획**
- **잘된 점**: FastAPI와 Streamlit의 통합으로 빠르고 직관적인 시스템 완성
- **아쉬운 점**: 핵심 목표였던 분석 결과를 텍스트 파일로 다운로드 기능 구현하지 못함
- **향후 계획**: 시장 매출 분석 데이터를 확장, 모델 정교화를 통해 성능 개선

---

## 🔧 기술 스택

| 기술         | 상세 내용              |
|--------------|-----------------------|
| **언어**     | Python               |
| **라이브러리** | Streamlit, LangChain, Pandas |
| **프레임워크** | FastAPI             |
| **버전 관리** | Git, GitHub          |

---

## 📂 결과물

- **사용자 인터페이스**: Streamlit 기반 대화형 챗봇
