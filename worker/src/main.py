'''
A service that manages requests for recipes.
'''

from fastapi import FastAPI
from pydantic import BaseModel
import json
import os
import typing
from langchain.vectorstores import Redis
from langchain.embeddings.huggingface import HuggingFaceEmbeddings

with open("/config/.config.json", "r") as f:
    CONFIG = json.load(f)
    REDIS_URL = CONFIG["worker"]["redis_url"]
    REDIS_INDEX = CONFIG["worker"]["redis_index"]

class Recipe(BaseModel):
    title: str
    ingredients: str
    instructions: str
    picture_link: str | None = None

embedder = HuggingFaceEmbeddings(
    model_name="sentence-transformers/multi-qa-mpnet-base-dot-v1",
    cache_folder="/models",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': False}
)

rds = Redis.from_existing_index(
    embedder,
    index_name=REDIS_INDEX,
    redis_url=REDIS_URL,
    schema="redis_schema.yaml",
)

app = FastAPI()

@app.post("/add_recipe/")
async def add_recipe(recipe: Recipe):
    text = recipe.title
    metadata = {
        "ingredients":recipe.ingredients,
        "instructions":recipe.instructions,
        "picture_link":recipe.picture_link,
    }

    data = '\n\n'.join([recipe.title, recipe.ingredients, recipe.instructions])
    embedding = embedder.embed_query(data)

    rds.add_texts(
        texts = [text],
        metadatas = [metadata],
        embeddings = [embedding],
    )

@app.get("/get_recipes/")
async def get_recipes(user_input: str = "French Recipe", limit: int = 10):

    recipes_raw = rds.similarity_search(user_input, k=limit, return_metadata=True)
    
    recipes = []

    # format recipes to Recipe class
    for r in recipes_raw:
        recipes.append({
            "title": r.page_content,
            "ingredients": r.metadata["ingredients"],
            "instructions": r.metadata["instructions"],
            "picture_link": r.metadata["picture_link"]
        })

    return recipes