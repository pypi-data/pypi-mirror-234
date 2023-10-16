from kasumi import KasumiEmbedding, Kasumi, KasumiConfigration
from random import random
import sys

def random_vector():
    return [random() for _ in range(1536)]

def test_vector_database():
    token = input("Please input your token: ")

    app = Kasumi(
        KasumiConfigration(
            app_id=8,
            token=token,
            search_key="123",
            kasumi_url="http://localhost:8192",
        )
    )

    embedding_dict = [
        { 'id': '1', 'embedding': app.embeding_text("穷"), 'text': '穷' },
        { 'id': '2', 'embedding': app.embeding_text("富"), 'text': '富' },
        { 'id': '3', 'embedding': app.embeding_text("暴富"), 'text': '暴富' },
    ]

    app.insert_embedding(embedding_dict[0]['embedding'], embedding_dict[0]['id'])
    app.insert_embedding(embedding_dict[1]['embedding'], embedding_dict[1]['id'])
    app.insert_embedding(embedding_dict[2]['embedding'], embedding_dict[2]['id'])

    ranks = app.search_embedding_similarity(app.embeding_text('没钱'))
    
    for rank in ranks:
        for item in embedding_dict:
            if item['id'] == rank.id:
                print(f'text: {item["text"]}, similarity: {rank.get_similarity()}')

    app.del_embedding_by_id(embedding_dict[0]['id'])
    app.del_embedding_by_id(embedding_dict[1]['id'])
    app.del_embedding_by_id(embedding_dict[2]['id'])

    try:
        item = app.get_embedding_by_id(embedding_dict[0]['id'])
        return False
    except:
        return True