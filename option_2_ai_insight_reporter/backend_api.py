# [2안] AI Insight Reporter Backend
import os, operator, time, logging
from fastapi import FastAPI
from typing import Annotated, TypedDict
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_community.callbacks.manager import get_openai_callback
from dotenv import load_dotenv

load_dotenv()
os.environ["LANGCHAIN_PROJECT"] = "Option2_Insight_Reporter"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# 글로벌 객체 초기화
GLOBAL_LLM = None
TAVILY_TOOL = None

try:
    GLOBAL_LLM = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    logger.info("LLM initialized (GPT-4o-mini)")
except Exception as e:
    logger.error(f"Failed to initialize LLM: {e}")

try:
    TAVILY_TOOL = TavilySearchResults(k=3)
    logger.info("Tavily Search Tool initialized")
except Exception as e:
    logger.error(f"Failed to initialize Tavily Tool: {e}")

@tool
def fetch_news_and_summarize(topic: str):
    """지정된 주제에 대한 최신 뉴스를 웹에서 검색하고 핵심 내용을 요약합니다."""
    if TAVILY_TOOL:
        raw_data = TAVILY_TOOL.run(topic)
        prompt = f"다음 검색 결과를 바탕으로 '{topic}'에 대한 3가지 핵심 인사이트를 요약하세요: {raw_data}"
        return GLOBAL_LLM.invoke(prompt).content
    return "웹 검색 도구를 사용할 수 없습니다. API 키를 확인해 주세요."

@tool
def generate_trend_report(summary_text: str):
    """요약된 텍스트를 바탕으로 공식적인 트렌드 보고서 형식을 생성합니다."""
    prompt = f"다음 요약을 바탕으로 [트렌드 분석 보고서] 제목 하에 서론, 본문, 결론 구조로 문서를 작성하세요: {summary_text}"
    return GLOBAL_LLM.invoke(prompt).content

tools = [fetch_news_and_summarize, generate_trend_report]
llm_with_tools = None
if GLOBAL_LLM:
    llm_with_tools = GLOBAL_LLM.bind_tools(tools)

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]

def call_model(state: AgentState):
    sys_msg = SystemMessage(content="당신은 전문 뉴스 분석가이자 리포터입니다. 뉴스를 수집하여 고차원의 인사이트 보고서를 작성합니다.")
    if llm_with_tools:
        return {"messages": [llm_with_tools.invoke([sys_msg] + state['messages'])]}
    else:
        return {"messages": [HumanMessage(content="AI 모델 초기화 실패. API 키를 확인해 주세요.")]}

builder = StateGraph(AgentState)
builder.add_node("agent", call_model)
builder.add_node("action", ToolNode(tools))
builder.set_entry_point("agent")
builder.add_conditional_edges("agent", lambda x: "action" if x['messages'] and x['messages'][-1].tool_calls else END)
builder.add_edge("action", "agent")
graph_engine = builder.compile()

@app.post("/ask")
async def ask_api(query: str):
    with get_openai_callback() as cb:
        start_t = time.time()
        try:
            result = graph_engine.invoke({"messages": [HumanMessage(content=query)]})
            ans = result['messages'][-1].content
        except Exception as e:
            logger.error(f"Execution error: {e}")
            ans = f"오류 발생: {str(e)}"
            
        return {
            "answer": ans,
            "stats": {
                "latency": round(time.time() - start_t, 2),
                "total_tokens": cb.total_tokens,
                "total_cost": cb.total_cost,
                "timestamp": time.strftime("%H:%M:%S")
            }
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
