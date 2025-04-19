import numpy as np
import faiss
import pandas as pd
import ast

df1 = pd.read_csv('data1.csv')
df2 = pd.read_csv('data2.csv')

embeddings1 = df1['embedding'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x).tolist()
embeddings2 = df2['embedding'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x).tolist()

embeddings = embeddings1 + embeddings2
embeddings = np.array(embeddings).astype('float32')

index = faiss.IndexFlatL2(384)
index.add(embeddings)
faiss.write_index(index, "./data/vector_db.faiss")
