import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
import faiss
import numpy as np

load_dotenv("./MLAlgo/.env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_embeddings = OpenAIEmbeddings()

index = faiss.read_index("./MLAlgo/abstractIndex.index")
def prompt_embedding(prompt: str, num: int):
    inp = openai_embeddings.embed_query(prompt)
    inp = np.array([inp]).astype("float32")
    k = num
    distances, indices = index.search(inp, k)
    return indices.tolist()
