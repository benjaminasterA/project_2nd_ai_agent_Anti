# [3안] Personal Agent Hub Backend
import os, operator, time
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

app = FastAPI()
GLOBAL_LLM = ChatOpenAI(model="gpt-4o", temperature=0.7) # 좀 더 창의적인 추천을 위해 temp 상향

@tool
def personal_preference_search(query: str):
    """사용자의 과거 선호도나 저장된 개인 정보를 검색합니다."""
    # 실제로는 가상으로 "사용자는 시원한 파란색과 모던한 디자인을 선호함" 같은 정보를 리턴하게 함
    return "사용자 프로필: 파란색 선호, 미니멀리즘 디자인 추구, 매운 음식을 좋아함."

@tool
def web_recommendation_search(query: str):
    """최신 트렌드와 웹 정보를 바탕으로 추천 아이템을 검색합니다."""
    search = TavilySearchResults(k=2)
    return search.run(query)

tools = [personal_preference_search, web_recommendation_search]
llm_with_tools = GLOBAL_LLM.bind_tools(tools)

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]

def call_model(state: AgentState):
    sys_msg = SystemMessage(content="당신은 사용자의 취향을 완벽히 이해하는 퍼스널 AI 비서입니다. 개인 선호도와 웹 정보를 결합하여 최상의 추천을 제공하세요.")
    return {"messages": [llm_with_tools.invoke([sys_msg] + state['messages'])]}

builder = StateGraph(AgentState)
builder.add_node("agent", call_model)
builder.add_node("action", ToolNode(tools))
builder.set_entry_point("agent")
builder.add_conditional_edges("agent", lambda x: "action" if x['messages'][-1].tool_calls else END)
builder.add_edge("action", "agent")
graph_engine = builder.compile()

@app.post("/ask")
async def ask_api(query: str):
    with get_openai_callback() as cb:
        start_t = time.time()
        result = graph_engine.invoke({"messages": [HumanMessage(content=query)]})
        return {
            "answer": result['messages'][-1].content,
            "stats": {
                "latency": round(time.time() - start_t, 2),
                "total_tokens": cb.total_tokens,
                "total_cost": cb.total_cost,
                "timestamp": time.strftime("%H:%M:%S")
            }
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)
