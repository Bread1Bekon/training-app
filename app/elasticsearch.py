from elasticsearch import AsyncElasticsearch
from config import settings

es_client = AsyncElasticsearch(
    settings.ELASTICSEARCH_URL,
    basic_auth=(settings.ELASTICSEARCH_USER, settings.ELASTICSEARCH_PASSWORD),
    verify_certs=False,
    ssl_show_warn=False
)

async def get_elasticsearch() -> AsyncElasticsearch:
    return es_client