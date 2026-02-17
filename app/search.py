import logging

from elasticsearch import Elasticsearch

from app.config import settings

logger = logging.getLogger(__name__)

es_client = Elasticsearch(settings.elasticsearch_url)

INDEX_NAME = "reviews"

INDEX_SETTINGS = {
    "mappings": {
        "properties": {
            "shot_id": {"type": "integer"},
            "author": {"type": "keyword"},
            "status": {"type": "keyword"},
            "body": {"type": "text", "analyzer": "english"},
            "department": {"type": "keyword"},
        }
    }
}


async def ensure_index():
    try:
        if not es_client.indices.exists(index=INDEX_NAME):
            es_client.indices.create(index=INDEX_NAME, body=INDEX_SETTINGS)
            logger.info("Created Elasticsearch index: %s", INDEX_NAME)
    except Exception:
        logger.warning("Could not connect to Elasticsearch — search will be unavailable")


def clear_index() -> None:
    try:
        es_client.delete_by_query(
            index=INDEX_NAME,
            body={"query": {"match_all": {}}},
            refresh=True,
        )
    except Exception:
        logger.warning("Failed to clear Elasticsearch index")


def index_review(review) -> None:
    try:
        es_client.index(
            index=INDEX_NAME,
            id=str(review.id),
            document={
                "shot_id": review.shot_id,
                "author": review.author,
                "status": review.status.value if hasattr(review.status, "value") else review.status,
                "body": review.body,
                "department": review.department,
            },
        )
    except Exception:
        logger.warning("Failed to index review %s", review.id)


def search_reviews(query: str, size: int = 20) -> list[dict]:
    try:
        resp = es_client.search(
            index=INDEX_NAME,
            query={"match": {"body": query}},
            size=size,
        )
        return [
            {
                "id": int(hit["_id"]),
                "score": hit["_score"],
                **hit["_source"],
            }
            for hit in resp["hits"]["hits"]
        ]
    except Exception:
        logger.warning("Elasticsearch search failed")
        return []
