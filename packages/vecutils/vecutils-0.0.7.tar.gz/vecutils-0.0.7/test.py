import asyncio
import random

from vecutils import Vectorizer, batch_create_embeddings


async def embedding_fn(texts):
    await asyncio.sleep(1)

    if random.random() > 0.1:
        raise ValueError

    return [[i * [1]] for i in range(len(texts))]


async def main():
    texts = [f"{i}" * random.randint(1, 10) for i in range(100)]

    vectroizer = Vectorizer("http://localhost:9394/v1/embeddings", "moka-ai/m3e-base")

    results = await batch_create_embeddings(
        texts,
        embedding_fn=vectroizer.acreate_embeddings,
        batch_size=10,
        concurrency=5,
    )

    print(results)


if __name__ == "__main__":
    asyncio.run(main())
