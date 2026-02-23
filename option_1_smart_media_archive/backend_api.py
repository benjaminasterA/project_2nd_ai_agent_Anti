# [1안] Smart Media Archive Backend
import os, operator, time
from fastapi import FastAPI
from typing import Annotated, TypedDict
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_community.callbacks.manager import get_openai_callback
from dotenv import load_dotenv

load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Option1_Media_Archive"

app = FastAPI()
GLOBAL_LLM = ChatOpenAI(model="gpt-4o-mini", temperature=0)
GLOBAL_EMBEDDINGS = OpenAIEmbeddings()
VECTOR_DB = None

def initialize_vector_db():
    global VECTOR_DB
    index_name = "media_archive_index"
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    # 미디어 메타데이터나 가이드 문서
    target_files = ["media_tagging_guide.pdf", "archive_manual.pdf"]
    
    if os.path.exists(index_name):
        VECTOR_DB = FAISS.load_local(index_name, GLOBAL_EMBEDDINGS, allow_dangerous_deserialization=True)
    else:
        if not os.path.exists(data_dir): os.makedirs(data_dir)
        # 예시 문서가 없을 때를 대비한 처리
        print("신규 인덱스 생성을 위한 데이터 준비가 필요합니다.")

initialize_vector_db()

@tool
def search_media_meta(query: str):
    """미디어 아카이브 저장소에서 관련 태그 및 메타데이터를 검색합니다."""
    if VECTOR_DB is None: return "아카이브 인덱스가 비어 있습니다."
    docs = VECTOR_DB.similarity_search(query, k=3)
    return "\n\n".join([d.page_content for d in docs])

@tool
def analyze_visual_content(description: str):
    """입력된 미디어 묘사를 바탕으로 AI가 자동 태그를 생성하고 분석합니다."""
    prompt = f"다음 미디어 묘사를 분석하여 5개의 키워드와 카테고리를 추출하세요: {description}"
    return GLOBAL_LLM.invoke(prompt).content

tools = [search_media_meta, analyze_visual_content]
llm_with_tools = GLOBAL_LLM.bind_tools(tools)

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]

def call_model(state: AgentState):
    sys_msg = SystemMessage(content="당신은 지능형 미디어 아카이브 전문가입니다. 사용자의 미디어를 분석하고 보관된 정보를 찾아줍니다.")
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
    uvicorn.run(app, host="127.0.0.1", port=8003)
