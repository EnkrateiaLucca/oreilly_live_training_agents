import click
from typing import List
from typing_extensions import TypedDict
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import StrOutputParser
from langchain import hub
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph, START
from pprint import pprint
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings


MODEL = 'gpt-4o-mini'

# Data models for grading
class GradeDocuments(BaseModel):
    binary_score: str = Field(description="Documents are relevant to the question, 'yes' or 'no'")

class GradeHallucinations(BaseModel):
    binary_score: str = Field(description="Answer is grounded in the facts, 'yes' or 'no'")

class GradeAnswer(BaseModel):
    binary_score: str = Field(description="Answer addresses the question, 'yes' or 'no'")

class GraphState(TypedDict):
    question: str
    generation: str
    documents: List[str]


def setup_retriever(file_path='./relevant-sources/AI-Act.pdf'):
    docs_list = PyPDFLoader(file_path).load()

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=250, chunk_overlap=0
    )
    doc_splits = text_splitter.split_documents(docs_list)

    # Add to vectorDB
    vectorstore = Chroma.from_documents(
        documents=doc_splits,
        collection_name="rag-chroma-ai-act",
        embedding=OpenAIEmbeddings(),
    )
    retriever = vectorstore.as_retriever()
    
    return retriever

# Initialize LLMs
retriever = setup_retriever()
retrieval_llm = ChatOpenAI(model=MODEL, temperature=0)
generation_llm = ChatOpenAI(model=MODEL, temperature=0)
grading_llm = ChatOpenAI(model=MODEL, temperature=0)

# Prompts
grade_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a grader assessing relevance of a retrieved document to a user question."),
    ("human", "Retrieved document: \n\n {document} \n\n User question: {question}")
])
hallucination_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a grader assessing whether an LLM generation is grounded in a set of retrieved facts."),
    ("human", "Set of facts: \n\n {documents} \n\n LLM generation: {generation}")
])
answer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a grader assessing whether an answer addresses a question."),
    ("human", "User question: \n\n {question} \n\n LLM generation: {generation}")
])
question_rewriter_prompt = ChatPromptTemplate.from_messages([
    ("system", "You a question re-writer that converts an input question to a better version."),
    ("human", "Here is the initial question: \n\n {question} \n Formulate an improved question.")
])

# Chain
# Prompt
prompt = hub.pull("rlm/rag-prompt")
# LLM
llm = ChatOpenAI(model_name=MODEL, temperature=0)
rag_chain = prompt | llm | StrOutputParser()
# Chains
retrieval_grader = grade_prompt | retrieval_llm.with_structured_output(GradeDocuments)
hallucination_grader = hallucination_prompt | grading_llm.with_structured_output(GradeHallucinations)
answer_grader = answer_prompt | grading_llm.with_structured_output(GradeAnswer)
question_rewriter = question_rewriter_prompt | retrieval_llm | StrOutputParser()

# Functions for the workflow
def retrieve(state):
    """Retrieve documents based on the provided question."""
    print("---RETRIEVE---")
    state["documents"] = retriever.get_relevant_documents(state["question"])
    return state

def generate(state):
    """Generate an answer based on the retrieved documents."""
    print("---GENERATE---")
    generation = rag_chain.invoke({"context": state["documents"], "question": state["question"]})
    state["generation"] = generation
    return state

def grade_documents(state):
    """Grade retrieved documents and filter relevant ones."""
    print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
    filtered_docs = [d for d in state["documents"] if retrieval_grader.invoke({"question": state["question"], "document": d.page_content}).binary_score == "yes"]
    state["documents"] = filtered_docs
    return state

def transform_query(state):
    """Transform the input question to improve retrieval."""
    print("---TRANSFORM QUERY---")
    state["question"] = question_rewriter.invoke({"question": state["question"]})
    return state

def decide_to_generate(state):
    """Decide whether to generate an answer or re-generate a query."""
    return "transform_query" if not state["documents"] else "generate"

def grade_generation(state):
    """Check if the generated answer is grounded in the retrieved documents and addresses the question."""
    print("---CHECK HALLUCINATIONS---")
    hallucination_score = hallucination_grader.invoke({"documents": state["documents"], "generation": state["generation"]})
    if hallucination_score.binary_score == "yes":
        answer_score = answer_grader.invoke({"question": state["question"], "generation": state["generation"]})
        return "useful" if answer_score.binary_score == "yes" else "not useful"
    return "not supported"

# Setting up the graph
workflow = StateGraph(GraphState)
workflow.add_node("retrieve", retrieve)
workflow.add_node("grade_documents", grade_documents)
workflow.add_node("generate", generate)
workflow.add_node("transform_query", transform_query)

workflow.add_edge(START, "retrieve")
workflow.add_edge("retrieve", "grade_documents")
workflow.add_conditional_edges("grade_documents", decide_to_generate, {"transform_query": "transform_query", "generate": "generate"})
workflow.add_edge("transform_query", "retrieve")
workflow.add_conditional_edges("generate", grade_generation, {"not supported": "generate", "useful": END, "not useful": "transform_query"})

app = workflow.compile()

@click.command()
@click.option('--question', prompt='Enter your question', help='The question to be assessed.')
def run_workflow(question):
    """A CLI for processing large language model retrieval and grading workflow."""
    inputs = {"question": question, "documents": []}
    for output in app.stream(inputs):
        for key, value in output.items():
            pprint(f"Node '{key}': {value}")
    
    print("Answer")
    pprint(value["generation"])

if __name__ == "__main__":
    run_workflow()