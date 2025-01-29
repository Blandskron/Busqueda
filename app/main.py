from fastapi import FastAPI, Query
from elasticsearch import Elasticsearch
from pydantic import BaseModel
from typing import List, Optional

# Definir las variables de configuración
ES_SCHEME = "http"  # Agregar el protocolo
ES_HOST = "localhost"  # El nombre del host de Elasticsearch
ES_PORT = 9200  # El puerto de Elasticsearch
# Define el nombre del índice
INDEX_NAME = "documents_index"

# Inicializar Elasticsearch con los parámetros correctos
es = Elasticsearch([{'scheme': ES_SCHEME, 'host': ES_HOST, 'port': ES_PORT}])
app = FastAPI()

# Verificar que Elasticsearch esté en funcionamiento
if not es.ping():
    raise Exception("Elasticsearch no está disponible.")

# Modelo Pydantic para la estructura de los documentos
class Document(BaseModel):
    hashName: str
    path: str
    title: str
    type: str
    sizeBytes: int
    userId: int
    metadata: dict

@app.get("/search/")
async def search(query: str, size: int = Query(10, le=100)):
    """
    Endpoint para buscar documentos en Elasticsearch usando un query de texto.
    """
    # Definimos la consulta en Elasticsearch
    script_query = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title^2", "metadata.dc:title^1.5", "path^1", "type^1"]
            }
        },
        "size": size
    }

    try:
        # Realizamos la búsqueda en Elasticsearch
        response = es.search(index=INDEX_NAME, body=script_query)

        # Verificamos si la respuesta contiene hits
        if 'hits' not in response or 'hits' not in response['hits']:
            return {"error": "No hits found."}

        # Procesamos la respuesta
        results = []
        for hit in response['hits']['hits']:
            document = {
                "id": hit["_id"],
                "title": hit["_source"].get("title", "N/A"),
                "path": hit["_source"].get("path", "N/A"),
                "metadata": hit["_source"].get("metadata", {}),
                "score": hit["_score"]
            }
            results.append(document)

        return {"results": results}

    except Exception as e:
        return {"error": str(e)}

# Endpoint para agregar documentos
@app.post("/index_document/")
async def index_document(document: Document):
    """
    Endpoint para indexar un documento en Elasticsearch.
    """
    try:
        response = es.index(index=INDEX_NAME, document=document.dict())
        return {"message": "Document indexed successfully", "id": response['_id']}
    except Exception as e:
        return {"error": str(e)}
