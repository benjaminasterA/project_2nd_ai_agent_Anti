# [3안] Personal Agent Hub Backend
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
os.environ["LANGCHAIN_PROJECT"] = "Option3_Personal_Agent"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# 글로벌 객체 초기화
GLOBAL_LLM = None
TAVILY_TOOL = None

try:
    GLOBAL_LLM = ChatOpenAI(model="gpt-4o", temperature=0.7)
    logger.info("LLM initialized (GPT-4o)")
except Exception as e:
    logger.error(f"Failed to initialize LLM: {e}")

try:
    TAVILY_TOOL = TavilySearchResults(k=3)
    logger.info("Tavily Search Tool initialized")
except Exception as e:
    logger.error(f"Failed to initialize Tavily Tool: {e}")

@tool
def personal_preference_search(query: str):
    """사용자의 과거 선호도나 저장된 개인 정보를 검색합니다."""
    return "사용자 프로필: 파란색 선호, 미니멀리즘 디자인 추구, 매운 음식을 좋아함."

@tool
def web_recommendation_search(query: str):
    """최신 트렌드와 웹 정보를 바탕으로 추천 아이템을 검색합니다."""
    if TAVILY_TOOL:
        return TAVILY_TOOL.run(query)
    return "웹 검색 도구를 사용할 수 없습니다. (API 키 확인 필요)"

tools = [personal_preference_search, web_recommendation_search]
llm_with_tools = None
if GLOBAL_LLM:
    llm_with_tools = GLOBAL_LLM.bind_tools(tools)

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]

def call_model(state: AgentState):
    sys_msg = SystemMessage(content="당신은 사용자의 취향을 완벽히 이해하는 퍼스널 AI 비서입니다. 개인 선호도와 웹 정보를 결합하여 최상의 추천을 제공하세요.")
    if llm_with_tools:
        return {"messages": [llm_with_tools.invoke([sys_msg] + state['messages'])]}
    else:
        return {"messages": [HumanMessage(content="AI 모델 초기화에 실패했습니다. API 키 설정을 확인해 주세요.")]}

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
            ans = result['messages'][-1].content if result['messages'] else "응답을 생성할 수 없습니다."
        except Exception as e:
            logger.error(f"Graph execution error: {e}")
            ans = f"에이전트 실행 중 오류가 발생했습니다: {str(e)}"
            
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
    uvicorn.run(app, host="127.0.0.1", port=8004)
