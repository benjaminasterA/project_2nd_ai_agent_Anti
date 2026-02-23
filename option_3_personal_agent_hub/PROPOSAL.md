# [제안서] 퍼스널 에이전트 허브 (Personal Agent Hub)

## 1. 개요 (Overview)
본 프로젝트는 **LangGraph**를 활용하여 사용자와 상호작용하며 최적의 추천과 의사결정을 지원하는 멀티 에이전트 시스템입니다. 단순한 챗봇을 넘어, 추론(Reasoning)과 도구 활용(Tool Use)을 통해 복합적인 문제를 해결합니다.

## 2. 핵심 목표 (Core Objectives)
- **지능형 추론**: 사용자의 요청 뒤에 숨겨진 의도(Intent)를 파악하여 최적의 제안 도출.
- **워크플로우 제어**: LangGraph를 통해 에이전트 간의 순환 루프 및 상태 관리를 최적화.
- **실시간 확장**: 다양한 외부 도구(API)와의 연동을 통한 실용성 극대화.

## 3. 주요 기능 (Key Features)
- 페르소나 기반의 커스텀 추천 챗봇.
- 검색, 분석, 최종 제안을 수행하는 Multi-Agent 워크플로우.
- 메모리 유지 로직을 통한 장기적인 사용자 취향 학습.

## 4. 기술 스택 (Tech Stack)
- **Frontend**: React (Vite), Framer Motion (애니메이션).
- **Backend**: FastAPI (Python), LangGraph.
- **AI**: GPT-4o (Reasoning), Llama-3 (Groq API).
- **Database**: Qdrant (User Preference), PostgreSQL (Chat History).
