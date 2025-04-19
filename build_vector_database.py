import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import json

with open("./data/dataset.json", 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

questions = list(raw_data.keys())

model = SentenceTransformer("BAAI/bge-small-en-v1.5")

embeddings = np.array([model.encode(question).tolist() for question in questions])
df = pd.DataFrame({
    "chunk_id": range(1, len(questions) + 1),
    "text": questions,
    "embedding": [json.dumps(emb.tolist()) for emb in embeddings],
})

df.to_csv("data.csv", index=False, encoding="utf-8")
