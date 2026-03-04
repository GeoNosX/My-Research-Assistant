from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

# Import our state schemas
from .state import Re_State, QuestionState

# Import all the node functions
from .nodes import (
    create_researchers,
    start_questions, 
    make_question,
    web_search,
    wiki_search,
    expert,
    writer,
    my_condition_edge
)

# ==========================================
# 1. Graph: Create Researchers
# ==========================================
researcher_builder = StateGraph(Re_State)
researcher_builder.add_node('create_researchers', create_researchers)
researcher_builder.add_edge(START, 'create_researchers')
researcher_builder.add_edge('create_researchers', END)
researcher_graph = researcher_builder.compile()

# ==========================================
# 2. Graph: The Research & QA Process
# ==========================================
qa_builder = StateGraph(QuestionState)

# Add all the nodes
qa_builder.add_node('make_question', make_question)
qa_builder.add_node('web_search', web_search)
qa_builder.add_node('wiki_search', wiki_search)
qa_builder.add_node('expert', expert)
qa_builder.add_node('writer', writer)

# Connect the nodes with edges
qa_builder.add_edge(START, 'make_question')

# After a question is asked, search both web and wiki in parallel
qa_builder.add_edge('make_question', 'web_search')
qa_builder.add_edge('make_question', 'wiki_search')

# Both searches feed their context to the expert
qa_builder.add_edge('web_search', 'expert')
qa_builder.add_edge('wiki_search', 'expert')

# The expert answers, and we check our custom condition
qa_builder.add_conditional_edges(
    'expert',
    my_condition_edge,
    ['writer', 'make_question']
)

# The writer finishes the report and ends the workflow
qa_builder.add_edge('writer', END)

# Add memory so the graph remembers the conversation history
memory = MemorySaver()

# Compile the final graph
qa_graph = qa_builder.compile(checkpointer=memory)