# core/extractor.py

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda


# =========================
# Ollama LLM
# =========================

def get_llm():

    return ChatOllama(
        model="llama3.1:8b",
        temperature=0.2
    )


# =========================
# Build Chain
# =========================

def build_chain(system_prompt: str):

    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{text}")
    ])

    return (
        RunnablePassthrough()
        | RunnableLambda(lambda x: {"text": x})
        | prompt
        | llm
        | StrOutputParser()
    )


# =========================
# Extract Action Items
# =========================

def extract_action_items(transcript: str) -> str:

    chain = build_chain(
        """You are an expert meeting analyst.

From the meeting transcript, extract all action items.

For each action item provide:
- Task description
- Owner (who is responsible)
- Deadline (if mentioned, otherwise write 'Not specified')

Format the result as a numbered list.

If no action items are found, say:
'No action items found.'"""
    )

    return chain.invoke(transcript)


# =========================
# Extract Key Decisions
# =========================

def extract_key_decisions(transcript: str) -> str:

    chain = build_chain(
        """You are an expert meeting analyst.

From the meeting transcript, extract all key decisions that were made.

Format the result as a numbered list.

If no key decisions are found, say:
'No key decisions found.'"""
    )

    return chain.invoke(transcript)


# =========================
# Extract Open Questions
# =========================

def extract_questions(transcript: str) -> str:

    chain = build_chain(
        """You are an expert meeting analyst.

From the meeting transcript, extract all unresolved questions
or topics that need follow-up.

Format the result as a numbered list.

If no open questions are found, say:
'No open questions found.'"""
    )

    return chain.invoke(transcript)