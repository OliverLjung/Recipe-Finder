"""
Populate redis DB with pre-processed data
"""

import os
import pandas as pd
from langchain.vectorstores import Redis
from langchain.embeddings.huggingface import HuggingFaceEmbeddings

embedder = HuggingFaceEmbeddings(
    model_name="sentence-transformers/multi-qa-mpnet-base-dot-v1",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': False}
)

rds = Redis(
    redis_url = "redis://localhost:6379", 
    index_name = "recipes", 
    embedding = embedder
)

df = pd.read_json(f"{os.getcwd()}/data/data_clean.json")

texts = list(df["title"].values)
metadata = list(df[["ingredients", "instructions", "picture_link"]].apply(lambda row: {
    "ingredients":row.values[0],
    "instructions":row.values[1],
    "picture_link":row.values[2],
    }, axis=1).values)
embeddings = list(df["embedding"].values)

print(texts[:2])
print(metadata[:2])
print(embeddings[:2])

print(type(texts[1]))
print((metadata[1]["ingredients"]))
print(type(embeddings[1]))

rds.add_texts(
    texts = texts,
    metadatas = metadata,
    embeddings = embeddings
)