# [행동 요령] 스마트 미디어 아카이브 개발 가이드

본 개발 가이드는 프로젝트의 효율적인 진행과 유지보수를 위한 세부 행동 지침입니다.

## 1. 개발 착수 전 (Preparation)
- [ ] **환경 설정**: `.env` 파일을 생성하여 API Key (OpenAI, Qdrant 등)를 안전하게 관리합니다.
- [ ] **가상 환경**: `python -m venv venv`를 통해 독립적인 백엔드 환경을 구축합니다.

## 2. 단계별 행동 요령### [Step-by-Step Actions]
1.  **Backend Execution**: Run `py backend_api.py`. (Port: 8003)
2.  **Frontend Execution**: Run `streamlit run frontend_ui.py`.
3.  **Interaction**: Ask questions about media (e.g., "Find blue sky photos").

### Phase 2: 데이터 처리 엔진 개발
- 이미지 업로드 API를 구현합니다.
- 업로드된 파일에서 Vision API를 호출하여 태그를 생성하는 로직을 모듈화합니다.
- **효율성 Tip**: 대용량 비디오의 경우 프레임 샘플링 기법을 사용하여 분석 비용을 절감합니다.

### Phase 3: 벡터 인덱싱 및 검색
- 추출된 태그와 메타데이터를 벡터화하여 Qdrant에 저장합니다.
- 사용자 질문을 벡터화하여 유사한 미디어를 찾는 검색 API를 구현합니다.

## 3. 유지보수 및 기록 (Maintenance)
- 매 기능 완료 시마다 `HISTORY.md`에 변경 사항을 기록합니다.
- 코딩 중 발생하는 주요 에러와 해결법은 지식 베이스(KB)로 별도 관리할 것을 권장합니다.
