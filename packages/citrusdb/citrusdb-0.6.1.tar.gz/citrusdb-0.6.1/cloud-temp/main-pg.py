import os
import numpy as np
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import citrusdb

app = FastAPI()

PG_HOST = os.getenv("CITRUS_PG_HOST", None)
PG_PORT = os.getenv("CITRUS_PG_PORT", 5432)
PG_USER = os.getenv("CITRUS_PG_USER", "postgres")
PG_PASSWORD = os.getenv("CITRUS_PG_PASSWORD", )

client = citrusdb.Client(
    persist_directory="citrus-data/pg",
    database_type="pg",
    host=PG_HOST,
    port=PG_PORT,
    user=PG_USER,
    password=PG_PASSWORD
)

client.reload_indices()

@app.post("/index")
def create_index(index_name: str, max_elements: int = 1000, allow_replace_deleted: bool = True, M = 64, ef_construction = 200):
    try:
        client.create_index(
            name=index_name,
            max_elements=int(max_elements),
            allow_replace_deleted=allow_replace_deleted,
            M=int(M),
            ef_construction=int(ef_construction)
        )
        return {"message": f"Index '{index_name}' created successfully."}
    except Exception as error:
        return JSONResponse(status_code=500, content=error)

@app.post("/insert")
def insert_elements(index_name: str, elements: list[dict]):
    try:
        embeddings = None
        texts = None
        ids = [element["id"] for element in elements]

        keys = elements[0].keys()
        if "embedding" in keys:
            embeddings = np.asarray([element["embedding"] for element in elements], np.float32)
        if "text" in keys:
            texts = [element["text"] for element in elements]

        metadatas = [element["metadata"] for element in elements]

        client.add(index=index_name, ids=ids, embeddings=embeddings, documents=texts, metadatas=metadatas)
        return {"message": f"{len(ids)} vectors indexed."}
    except Exception as error:
        return JSONResponse(status_code=500, content=error)

@app.post("/search")
def semantic_search(index_name: str, search: dict, k: int = 1):
    try:
        embeddings = None
        text = None
        keys = search.keys()
        if "embedding" in keys:
            embeddings = np.asarray([search["embedding"]])
        if "text" in keys:
            text = [search["text"]]

        res = client.query(index=index_name, documents=text, query_embeddings=embeddings, k=k)
        if res:
            results, distances = res
            response = []
            for i, result in enumerate(results):
                for j, id in enumerate(result):
                    obj = {"id": int(id), "similarity_score": 1 - distances[i][j]}
                    response.append(obj)  # Assuming documents is accessible here
            return {"results": response}
    except Exception as error:
        return JSONResponse(status_code=500, content=error)

'''
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
