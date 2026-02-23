# [행동 요령] 퍼스널 에이전트 허브 개발 가이드

## 1. 개발 착수 전 (Preparation)
- [ ] **에이전트 역할 정의**: 검색 전문가, 품질 검수 전문가, 상담 전문가 등 필요한 에이전트의 페르소나를 정의합니다.
- [ ] **그래프 설계**: LangGraph로 구현할 상태(State)와 노드(Node) 간의 흐름도를 미리 스케치합니다.

## 2. 단계별 행동 요령### [Step-by-Step Actions]
1.  **Backend Execution**: Run `py backend_api.py`. (Port: 8004)
2.  **Frontend Execution**: Run `streamlit run frontend_ui.py`.
3.  **Interaction**: Ask for personal recommendations (e.g., "Recommend a restaurant based on my taste").

### Phase 1: LangGraph 기초 구현
- 상태 변수(State)를 정의하고 가장 단순한 환류 루프(Feedback Loop)를 먼저 테스트합니다.
- **주의**: 에이전트가 무한 루프에 빠지지 않도록 최대 반복 횟수(Recursion Limit)를 설정합니다.
- **Backend Port**: 8002번을 기본으로 사용합니다.

### Phase 2: 도구 연동 (Tool Integration)
- 검색(Serper), 계산, 날씨 등 에이전트가 사용할 수 있는 도구들을 정의합니다.
- LLM이 적절한 상황에 도구를 호출(Selection)하는지 집중적으로 테스트합니다.

### Phase 3: 사용자 경험 고도화
- 챗봇의 응답 속도를 개선하기 위해 스트리밍(Streaming) 기능을 구현합니다.
- 사용자의 과거 대화를 기억하고 이를 추천에 반영하는 장기 메모리(Long-term Memory) 시스템을 벡터 DB와 연동합니다.

## 3. 유지보수 및 기록 (Maintenance)
- 프롬프트 엔지니어링 수행 결과를 `HISTORY.md`에 기록하여 성능 변화를 추적합니다.
- 새로운 에이전트나 도구가 추가될 때마다 행동 요령의 그래프 설계 섹션을 최신화합니다.
