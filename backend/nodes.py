from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.document_loaders import WikipediaLoader
from langgraph.types import Send

# Import our state schemas and the LLM we just set up
from .state import Re_State, QuestionState, Res_List, SearchQuery
from .llm import llm





# Initialize the Serper API wrapper
serper_search = GoogleSerperAPIWrapper()
tavily_search_tool= TavilySearchResults(max_results=1)

def create_researchers(state: Re_State):
    llm_with_structure = llm.with_structured_output(Res_List)
    prompt = ChatPromptTemplate.from_messages([
        ('system', """You are tasked with creating a set of researchers 
         that they are specialized in: {topic}.
        1. First read carefully the topic:\n {topic}
        2. Determine the most interesting themes based upon documents.
        3. Pick the top {max_researchers} themes."""),
        ('user', " Generate the set of researchers")
    ])
    
    output = llm_with_structure.invoke(
        prompt.format_prompt(topic=state['topic'], max_researchers=state['max_researchers']).to_messages()
    )
    return {'re_list': output.re_list}

def start_questions(state: Re_State):
    """This triggers the parallel question branches for each researcher."""
    topic = state['topic']
    return [Send('make_question', {
        'researcher': researcher, 
        'topic_description': topic,
        'context': [],
        'questions_answer': []
    }) for researcher in state['re_list']]

def make_question(state: QuestionState):
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a researcher with the following profile:\n
       {self_info} \n
       Your role is to engage an expert in conversation about a topic.
       - Ask precise, insightful questions that go beyond generalities.
       - Aim to uncover surprising, scientifically grounded insights.
       - Continuously refine your questions to drill deeper into the subject.
       - Stay in character at all times, reflecting the profile and goals described above.
       - Ask only the question do not try to explain why you ask this question.

       - To maintain context, here is the history of your conversation with the expert:
       \n{conversation}\n

       - When you are fulfilled with the expert's answer, you answer him: 'Thank you for your time, that helped me a lot.' """),
        ('user', 'Ask a question to the expert about {topic}')
    ])
    question = llm.invoke(
        prompt.format_prompt(
            self_info=state['researcher'].description,
            topic=state['topic_description'],
            conversation=state['questions_answer']
        ).to_messages()
    )
    return {'questions_answer': [f'question: {question.content}']}

def web_search(state: QuestionState):
    prompt = ChatPromptTemplate.from_messages([
        ('system', """Given a conversation between a researcher and an expert on the {topic} your 
         job is generate a query in order use it in a web-search related to that convertation.
        1. Pay attention to the questions posed by the researcher.
        2. Analyze the conversation carefully.
        3. Convert researcher's final question into a web search query.
        4. Output only the search query.
        Here is the conversation for you to see: {conversation}""")
    ])
    search_llm = llm.with_structured_output(SearchQuery)
    query = search_llm.invoke(
        prompt.format_prompt(topic=state['topic_description'], conversation=state['questions_answer']).to_messages()
    )
    search_output = serper_search.run(query.search)
    return {'context': [search_output]}


def Tavily_search(state: QuestionState):
    prompt = ChatPromptTemplate.from_messages([
        ('system', """Given a conversation between a researcher and an expert on the {topic} your 
         job is generate a query in order use it in a web-search related to that convertation.
        1. Pay attention to the questions posed by the researcher.
        2. Analyze the conversation carefully.
        3. Convert researcher's final question into a web search query.
        4. Output only the search query.
        Here is the conversation for you to see: {conversation}""")
    ])
    search_llm = llm.with_structured_output(SearchQuery)
    query = search_llm.invoke(
        prompt.format_prompt(topic=state['topic_description'], conversation=state['questions_answer']).to_messages()
    )
    search_output = tavily_search_tool.run(query.search)
    return {'context': [search_output]}

def wiki_search(state: QuestionState):
    prompt = ChatPromptTemplate.from_messages([
        ('system', """Given a conversation between a researcher and an expert on the {topic} your 
         job is generate a query in order use it in a wikipedia search related to that convertation.
        1. Pay attention to the questions posed by the researcher.
        2. Analyze the conversation carefully.
        3. Convert researcher's final question into a wikipedia search query.
        4. Output only the search query.
        Here is the conversation for you to see: {conversation}""")
    ])
    search_llm = llm.with_structured_output(SearchQuery)
    query = search_llm.invoke(
        prompt.format_prompt(topic=state['topic_description'], conversation=state['questions_answer']).to_messages()
    )
    docs = WikipediaLoader(query.search, load_max_docs=2).load()
    if docs:
        search_output = docs[0].metadata.get('summary', docs[0].page_content[:500])
    else:
        search_output = "No relevant Wikipedia information found."
    return {'context': [search_output]}

def expert(state: QuestionState):
    prompt = ChatPromptTemplate.from_messages([
        ('system', """
# MISSION
You are a senior expert in {topic}. Your role is to answer a researcher's question with precision, using **only** the provided context.

# RESEARCHER PROFILE
{researcher_info}

# SOURCE CONTEXT \n
{context}\n

# INSTRUCTIONS
1.  **Source Fidelity:** Your answer must be derived solely from the provided context. This is non-negotiable. If the answer isn't in the context, you must state that it is not covered.
2.  **Tailor the Explanation:** Consider the researcher's background. If they are a specialist, use appropriate technical language. If they are a cross-disciplinary researcher, adjust the explanation to be accessible without losing scientific rigor.
3.  **Response Structure:**
    * **Direct Answer:** Begin with a concise, direct answer to the question.
    * **Detailed Explanation:** Elaborate on the answer, citing specific details, data, or mechanisms from the context.
    * **Contextual Link:** Where relevant, connect the answer to the broader field or the researcher's specific interests as hinted in their profile.
4.  **Maintain Scientific Integrity:** Present facts objectively. Differentiate between established findings (as per the context) and hypotheticals or suggested future directions (if mentioned in the context)."""),
        ('user', "{question}")
    ])
    answer = llm.invoke(
        prompt.format_prompt(
            researcher_info=state['researcher'].description,
            context=state['context'],
            question=state['questions_answer'][-1],
            topic=state['topic_description']
        ).to_messages()
    )
    return {'questions_answer': [f'answer: {answer.content}']}

def writer(state: QuestionState):
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a professional technical writer. Your task is to create a clear, well-structured report based on the provided documents.

Documents to analyze:
\n{documents}\n

Below is a conversation between a researcher and an expert. Based on the above documents.
\n {conversation}\n

Follow these rules when writing the report:
1. Format the report using **Markdown**:
   - Use `##` for section titles.
   - Use `###` for sub-section headers.
2. The report must include the following sections:
   - ## Title
   - ### Summary
3. The report should be **concise, objective, and professional**, with a maximum length of **500 words**.
4. Ensure the summary accurately reflects the main insights from the documents and experts answers."""),
        ("user", "Write a report based on the provided documents.")
    ])
    answer = llm.invoke(
        prompt.format_prompt(documents=state['context'], conversation=state['questions_answer']).to_messages()
    )
    return {'report': answer.content}

def my_condition_edge(state: QuestionState):
    max_questions = len(state['questions_answer'])
    # Added a simple string check to ensure we catch the 'Thank you' response reliably
    if 'Thank you for your time' in state['questions_answer'][-1] or max_questions > 4:
        return 'writer'
    else:
        return 'make_question'