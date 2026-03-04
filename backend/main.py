from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uuid

# Import our graphs AND the real Researchers model!
from backend.graph import researcher_graph, qa_graph
from backend.state import Researchers

app = FastAPI(title="Research Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Models

class TopicRequest(BaseModel):
    topic: str
    max_researchers: int = 3

class ResearchRequest(BaseModel):
    topic: str
    researcher: Researchers 

# API Endpoints

@app.get("/")
def read_root():
    return {"message": "Welcome to the Research Assistant Backend! It is running perfectly."}

@app.post("/create_researchers")
def api_create_researchers(req: TopicRequest):
    """Takes a topic and returns a list of AI-generated researchers."""
    state = {
        're_list': [],
        'topic': req.topic,
        'max_researchers': req.max_researchers
    }
    
    result = researcher_graph.invoke(state)
    return {"researchers": result['re_list']}

@app.post("/run_research")
def api_run_research(req: ResearchRequest):
    """Takes a topic and a specific researcher, runs the QA loop, and writes a report."""
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    state = {
        'context': [],
        'questions_answer': [],
        'researcher': req.researcher, 
        'topic_description': req.topic,
        'report': ""
    }
    
    result = qa_graph.invoke(state, config)
    
    return {
        "report": result.get('report', "No report generated."), 
        "conversation": result.get('questions_answer', [])
    }