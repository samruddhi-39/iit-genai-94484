from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from vectorstore import resume_retriever

@tool
def search_resume(job_description: str) -> str:
    """Tool for agent to retrieve top-K resumes."""
    return resume_retriever(job_description,top_k=3)

llm=init_chat_model(
    model="phi-3-mini-4k-instruct",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="dummy-key"
)

agent = create_agent(
    model=llm,
    tools=[search_resume],
    system_prompt="You are a helpful assistant. Use only the resumes provided to answer in detail."
)

def run_agent(query: str) -> str:
    """Run agent on job description using all top-K resumes combined with detailed explanation."""
    resume_text = resume_retriever(query, top_k=3)
    if resume_text == "No resumes found":
        return resume_text

    prompt = f"""
        You are a hiring assistant. A job description and candidate resumes are provided below.

        Job Description:{query}

        Candidate Resumes:{resume_text}

        Instructions:
        1. For each resume, provide a detailed assessment in the following format:

        Rank X: resume-ID

        [If it fits:]
        This resume fits the job description for the role. Here's a breakdown:
        - Experience: ...
        - Skills: ...
        - Experience Highlights: ...
        - Education: ...
        - Projects: ...
        - Overall: ...

        [If it does not fit:]
        This resume does not fit the job description. Here's why:
        - Focus/Experience: ...
        - Missing Skills: ...
        - Summary Highlights: ...
        - Overall: ...

        2. Be concise but detailed, highlighting key points from the resume only.
        3. Do not add any information not in the resume.
        4. Keep each resume assessment separated clearly.
        5. Rank the resumes from most relevant to least relevant.
    """
    result = agent.invoke({
        "messages": [{"role": "user", "content": prompt}]
    })
    ai_msg = result["messages"][-1]
    return ai_msg.content
