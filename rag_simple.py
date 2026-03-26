"""
Minimal RAG (Retrieval-Augmented Generation) example.

Flow: small knowledge base -> simple keyword overlap retrieval -> LLM answers
using only retrieved context (Ollama via your local openai stub).

Run:
  python3 rag_simple.py

Requires: Ollama running, model e.g. llama3.2 pulled.
"""

from __future__ import annotations

import re
from typing import List

from openai import OpenAI

OLLAMA_HOST = "http://localhost:11434"
CHAT_MODEL = "llama3.2"

# Pretend this is your "indexed" knowledge (in real apps: load from files + chunk).
KNOWLEDGE_CHUNKS: List[str] = [
    "A Lifetime ISA (LISA) lets UK residents aged 18–39 save up to £4,000 per tax year "
    "with a 25% government bonus, usable for a first home or retirement.",
    "First-time buyers in England may use a Help to Buy ISA legacy or LISA toward a deposit; "
    "rules and limits change—check gov.uk for current schemes.",
    "A typical mortgage deposit in the UK is often 5–15% of the property price; "
    "higher deposits can mean lower interest rates.",
    "Budgeting: track income, fixed costs, and discretionary spend; "
    "pay down high-interest debt before aggressive saving for a house.",
]


def tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def retrieve(query: str, chunks: List[str], top_k: int = 2) -> List[str]:
    """Very simple retrieval: score chunks by word overlap with the query."""
    q = tokenize(query)
    if not q:
        return chunks[:top_k]

    scored: List[tuple[int, str]] = []
    for ch in chunks:
        c = tokenize(ch)
        score = len(q & c)
        scored.append((score, ch))

    scored.sort(key=lambda x: x[0], reverse=True)
    # If all scores are 0, still return first chunks so the model has something.
    if scored[0][0] == 0:
        return chunks[:top_k]
    return [s[1] for s in scored[:top_k]]


def rag_answer(question: str) -> str:
    context_chunks = retrieve(question, KNOWLEDGE_CHUNKS, top_k=2)
    context = "\n\n".join(f"[{i+1}] {c}" for i, c in enumerate(context_chunks))

    system = (
        "You are a helpful assistant. Answer using ONLY the CONTEXT below. "
        "If the answer is not supported by the context, say you don't know."
    )
    user = f"CONTEXT:\n{context}\n\nQUESTION:\n{question}"

    client = OpenAI(base_url=OLLAMA_HOST)
    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    q = "What is a LISA and who can use it?"
    print("Question:", q)
    print()
    print(rag_answer(q))
