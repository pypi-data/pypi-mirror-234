from __future__ import annotations

# This file contains the functions used to insert and retrieve embeddings from the Kasumi database.
from typing import List, Union

from requests import post, get

from kasumi.abstract import AbstractKasumi, AbstractKasumiEmbeddingItem
from .abstract import *

class KasumiEmbeddingItem(AbstractKasumiEmbeddingItem):
    embedding: List[float] = []
    similarity: float = 0.0
    id: str = ""

    def __init__(self, embedding: List[float], id: str):
        self.embedding = embedding
        self.id = id

    def set_similarity(self, similarity: float) -> None:
        self.similarity = similarity

    def get_similarity(self) -> float:
        return self.similarity

class KasumiEmbedding(AbstractKasumiEmbedding):
    def __init__(self) -> None:
        pass

    def embedding_text(self, app: AbstractKasumi, text: str, token_type: TokenType, token: str):
        url = app._config.get_kasumi_url()
        response = post(f"{url}/v1/embedding", data={
            "text": text,
            "token_type": token_type.value,
            "token": token
        })
        if response.status_code != 200:
            raise KasumiException("Failed to embed text.")
        
        return response.json()['data']['embedding']

    def get_embedding_by_id(self, app: AbstractKasumi, id: str) -> KasumiEmbeddingItem:
        url = app._config.get_kasumi_url()
        response = post(f"{url}/v1/vec/get/via_id", data={
            'app_id': app._config.get_app_id(),
            'key': app._config.get_search_key(),
            'id': id
        })
        if response.status_code != 200:
            raise KasumiException(f"Failed to get embedding due to {response.text}")
        response = response.json()
        if response['code'] != 0:
            raise KasumiException(f"Failed to get embedding due to {response['msg']}")
        data = response['data']
        items = []
        for item in data:
            embedding_item = KasumiEmbeddingItem([], item['_id'])
            items.append(embedding_item)
        return items[0]
    
    def del_embedding_by_id(self, app: AbstractKasumi, id: str) -> bool:
        url = app._config.get_kasumi_url()
        response = post(f"{url}/v1/vec/del/via_id", data={
            'app_id': app._config.get_app_id(),
            'key': app._config.get_search_key(),
            'id': id
        })
        if response.status_code != 200:
            raise KasumiException(f"Failed to delete embedding due to {response.text}")
        response = response.json()
        if response['code'] != 0:
            raise KasumiException(f"Failed to delete embedding due to {response['msg']}")
        return response['data'] == 'OK'

    def insert_embedding(self, app: AbstractKasumi, embedding: List[float], id: str) -> bool:
        url = app._config.get_kasumi_url()
        response = post(f"{url}/v1/vec/insert", data={
            'app_id': app._config.get_app_id(),
            'key': app._config.get_search_key(),
            'id': id,
            'embedding': ','.join([str(x) for x in embedding])
        })
        if response.status_code != 200:
            raise KasumiException(f"Failed to insert embedding due to {response.text}")
        response = response.json()
        if response['code'] != 0:
            raise KasumiException(f"Failed to insert embedding due to {response['msg']}")
        return response['data'] == 'OK'

    def search_similarity(self, app: AbstractKasumi, embedding: List[float], top_k: int = 3) -> List[KasumiEmbeddingItem]:
        url = app._config.get_kasumi_url()
        response = post(f"{url}/v1/vec/search", data={
            'app_id': app._config.get_app_id(),
            'key': app._config.get_search_key(),
            'embedding': ','.join([str(x) for x in embedding]),
            'top_k': top_k
        })
        if response.status_code != 200:
            raise KasumiException(f"Failed to search embedding due to {response.text}")
        response = response.json()
        if response['code'] != 0:
            raise KasumiException(f"Failed to search embedding due to {response['msg']}")
        data = response['data']

        result = []
        for item in data:
            embedding_item = KasumiEmbeddingItem([], item['_id'])
            embedding_item.set_similarity(item['similarity'])
            result.append(embedding_item)
        return result