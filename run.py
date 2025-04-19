from sentence_transformers import SentenceTransformer
import faiss
import json
import numpy as np
from groq import Groq

client = Groq(api_key="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")


def get_answer_from_context(question: str, context_chunks: list[str]) -> str:
    context = "\n".join(context_chunks)
    prompt = f"""Question: {question}
                 Context: {context}
                 Answer:"""
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "Câu trả lời phải luôn là Tiếng Việt"},
            {"role": "user", "content": question},
            {"role": "assistant", "content": prompt}
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False
    )
    return response.choices[0].message.content


embedding_model = SentenceTransformer("BAAI/bge-small-en-v1.5")

with open("./data/dataset.json", "r", encoding="utf-8") as file:
    context_data = json.load(file)

context_keys = list(context_data.keys())
faiss_index = faiss.read_index("./data/vector_db.faiss")


def main():
    question = "Tôi thích lập trình thì nên học ngành gì của trường nào?"
    query_vector = np.array(embedding_model.encode([question], show_progress_bar=True)).astype("float32")
    _, top_indices = faiss_index.search(query_vector, k=3)
    matched_keys = [context_keys[i] for i in top_indices[0]]
    matched_contexts = [context_data[key] for key in matched_keys]
    answer = get_answer_from_context(question, matched_contexts)
    print(answer)


main()
