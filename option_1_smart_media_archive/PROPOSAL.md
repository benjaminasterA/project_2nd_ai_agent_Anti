# [제안서] 스마트 미디어 아카이브 (Smart Media Archive)

## 1. 개요 (Overview)
본 프로젝트는 사용자가 업로드하는 이미지와 비디오 등 미디어를 AI가 자동으로 분석하여 태깅하고, 단순 키워드 검색을 넘어 문맥 기반의 의미 검색(Semantic Search)이 가능하도록 구축하는 지능형 아카이빙 시스템입니다.

## 2. 핵심 목표 (Core Objectives)
- **자동화**: Vision-LLM을 활용하여 수동 태깅 작업 제거.
- **검색 고도화**: 벡터 검색을 통한 자연어 질의 지원 (예: "작년 여름 제주도에서 찍은 파란 하늘 사진").
- **효율성**: 클라우드 벡터 DB 사용을 통한 로컬 자원 점유 최소화.

## 3. 주요 기능 (Key Features)
- 미디어 메타데이터 자동 추출 및 멀티 태깅.
- RAG(Retrieval-Augmented Generation) 기반 미디어 정보 질의응답.
- 웹 기반 대시보드를 통한 시각적 관리.

## 4. 기술 스택 (Tech Stack)
- **Frontend**: React (Vite), Tailwind CSS.
- **Backend**: FastAPI (Python).
- **AI**: GPT-4o-mini (Vision API), LangChain.
- **Database**: Qdrant Cloud (Vector), PostgreSQL.
