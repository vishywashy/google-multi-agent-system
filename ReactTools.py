from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import ToolMessage,SystemMessage,BaseMessage, HumanMessage
from langchain_ollama.chat_models import ChatOllama
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, END


