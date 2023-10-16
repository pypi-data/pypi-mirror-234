import logging
import uuid
from collections.abc import Callable

from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
from utils import chunk

from vecutils import batch_create_embeddings

logger = logging.getLogger(__name__)


def get_existed_point_ids(
    qdrant: QdrantClient,
    index: str,
    id_field: str = "id",
    limit: int = 10000,
) -> set[str | int]:
    offset = None

    ids = set()
    while True:
        records, offset = qdrant.scroll(
            collection_name=index,
            limit=limit,
            offset=offset,
            with_payload=True,
            with_vectors=False,
        )
        ids = ids.union(x.payload[id_field] for x in records)

        if not offset:
            break

    return ids


def index_vectors(
    client: QdrantClient,
    index: str,
    docs: list[dict],
    embeddings: list[list[float]],
    vector: str | None = None,
) -> None:
    def _get_vector(embedding):
        if not vector:
            return embedding

        return {
            vector: embedding,
        }

    if len(docs) != len(embeddings):
        msg = "mismatched lengths of documents and embeddings: %d != %d"
        raise ValueError(msg, len(docs), len(embeddings))

    points = [
        PointStruct(
            id=uuid.uuid4().hex,
            vector=_get_vector(embedding),
            payload=doc,
        )
        for embedding, doc in zip(embeddings, docs, strict=True)
    ]
    client.upsert(collection_name=index, wait=True, points=points)


def batch_index_vectors(  # noqa: PLR0913
    client: QdrantClient,
    index: tuple[str, str],
    docs: list[dict],
    embedding_fn: Callable[[list[str]], list[list[float]]],
    index_chunk_size: int = 256,
    embedding_chunk_size: int = 16,
) -> None:
    index_name, vector_name = index

    for batch in chunk(docs, size=index_chunk_size):
        batch_embeddings = batch_create_embeddings(
            batch,
            embedding_fn=embedding_fn,
            batch_size=embedding_chunk_size,
        )
        if len(batch_embeddings) != len(batch):
            logger.warning(
                "%d / %d docs failed to create embeddings",
                len(batch) - len(batch_embeddings),
                len(batch),
            )

        if not batch_embeddings:
            continue

        indices, embeddings = zip(*batch_embeddings, strict=True)
        filtered_batch = [batch[i] for i in indices]

        logger.info("update %d embeddings to qdrant", len(indices))
        index_vectors(client, index_name, filtered_batch, embeddings, vector_name)
