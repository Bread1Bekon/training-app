from elasticsearch import Elasticsearch
from config import settings

client = Elasticsearch(
    settings.ELASTICSEARCH_URL,
    basic_auth=(settings.ELASTICSEARCH_USER, settings.ELASTICSEARCH_PASSWORD),
)
