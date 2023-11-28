"""
Simple data preprocessing for recipe finder
"""

import json
import pandas as pd
import os
import re
from sentence_transformers import SentenceTransformer

# Get data
def _get_dataset() -> pd.DataFrame:
    """
    Find all recipes in its directory
    """
    files = os.listdir(f"{os.getcwd()}/raw_data/recipes_raw")
    files = [f"{os.getcwd()}/raw_data/recipes_raw/{f}" for f in files if re.match(r'.*\.json$', f)]

    data = {
        "title":[],
        "ingredients":[],
        "instructions":[],
        "picture_link":[],
        }

    for f in files:
        with open(f, "r") as fp:
            d = json.load(fp)
            for r_id, recipe in d.items():
                if recipe == {}: continue
                try:
                    data["title"].append(recipe["title"])
                    data["ingredients"].append(recipe["ingredients"])
                    data["instructions"].append(recipe["instructions"])
                    data["picture_link"].append(recipe["picture_link"])
                except KeyError as e:
                    print(f"error:\n{e}\n\n for recipe:\n{r_id} -- {recipe}")
                    return

    dataset = pd.DataFrame(data)

    return dataset

# Clean data
def _clean_dataset(dataset:pd.DataFrame) -> pd.DataFrame:
    """
    Cleans dataset to serve for embedder
    """

    dataset["ingredients"] = dataset["ingredients"].apply("\n".join)

    ad_remover = lambda s: re.sub("ADVERTISEMENT", "", s) if isinstance(s, str) else s

    dataset["title"] = dataset["title"].apply(ad_remover)
    dataset["ingredients"] = dataset["ingredients"].apply(ad_remover)
    dataset["instructions"] = dataset["instructions"].apply(ad_remover)

    return dataset

# Embed data
def _embed_dataset(dataset:pd.DataFrame) -> pd.DataFrame:
    """
    Embeds the recipes for search
    """

    # https://huggingface.co/sentence-transformers/multi-qa-mpnet-base-dot-v1 
    model = SentenceTransformer("multi-qa-mpnet-base-dot-v1", device="cuda")

    # Credit to Allen: https://stackoverflow.com/a/52270276
    dataset["embedding"] = dataset[["title", "ingredients", "instructions"]].apply(lambda row: '\n\n'.join(row.values.astype(str)), axis=1)
    #

    dataset["embedding"] = dataset["embedding"].apply(model.encode)

    return dataset

import time
if __name__ == "__main__":
    df = _get_dataset()

    # limit dataset (development)
    df = df.iloc[:10000]
    #
    
    df = _clean_dataset(df)
    start_time = time.time()
    df = _embed_dataset(df)
    df.to_json(f"{os.getcwd()}/data/data_clean.json")