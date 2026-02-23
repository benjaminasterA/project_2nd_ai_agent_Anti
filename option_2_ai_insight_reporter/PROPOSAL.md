# [제안서] AI 인사이트 리포터 (AI Insight Reporter)

## 1. 개요 (Overview)
본 프로젝트는 인터넷상의 방대한 뉴스 데이터를 실시간으로 수집하고, AI를 통해 주제별로 분류(Clustering) 및 요약하여 사용자에게 필요한 맞춤형 보고서를 제공하는 시스템입니다.

## 2. 핵심 목표 (Core Objectives)
- **정보 노이즈 제거**: 유사/중복 기사를 하나로 통합하여 가독성 증대.
- **맞춤형 분석**: 사용자가 지정한 키워드나 산업 분야에 특화된 인사이트 추출.
- **비용 최적화**: 경량화된 LLM을 사용하여 고성능 요약 서비스 유지.

## 3. 주요 기능 (Key Features)
- 뉴스 RSS 및 웹 스크래퍼 기반 데이터 수집.
- 주제별 뉴스 클러스터링 및 계층적 요약.
- 일간/주간 인사이트 리포트 자동 생성 (PDF/이메일).

## 4. 기술 스택 (Tech Stack)
- **Frontend**: React (Vite), Chart.js (통계 시각화).
- **Backend**: FastAPI (Python), BeautifulSoup/Scrapy (수집).
- **AI**: GPT-4o-mini (Summary), Scikit-learn (Clustering).
- **Database**: PostgreSQL (News Meta), Redis (Cache).
