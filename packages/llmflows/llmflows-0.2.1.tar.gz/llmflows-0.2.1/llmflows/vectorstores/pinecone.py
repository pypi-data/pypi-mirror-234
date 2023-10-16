"""
Module to interact with Pinecone, a vector database service.

This module contains a class `Pinecone` which provides several methods to
interact with the Pinecone vector database service.
"""

import pinecone  # pylint: disable=import-error
from llmflows.vectorstores.vector_doc import VectorDoc
from llmflows.vectorstores.vector_store import VectorStore


class Pinecone(VectorStore):
    """
    Interact with Pinecone, a vector database service.

    This class has methods to initialize the Pinecone client, describe the index,
    search the index for similar vectors, and insert or update vectors in the index.

    Args:
        index_name (str): The name of the index to use.
        api_key (str): The Pinecone API key to use for authentication.
        environment (str): The environment to use, e.g. "production" or "development".
    
    Attributes:
        index_name (str): The name of the index to use.
        environment (str): The pinecone environment to use.
    """

    def __init__(self, index_name: str, api_key: str, environment: str):
        super().__init__(index_name, api_key, environment)
        self._init_client()

    def _prepare_results(self, search_result) -> tuple[list, dict, dict]:
        """
        Format the search results for the Pinecone vector store client.

        Args:
            search_result (dict): The search result returned by the Pinecone search.

        Returns:
            A tuple containing list of matches, the call parameters, and the pinecone 
                config.
        """
        search_results = search_result["matches"]

        call_data = {
            "raw_outputs": search_result,
        }

        config = {
            "environment": self.region,
            "index_name": self.storage_entity
        }

        return search_results, call_data, config

    def _init_client(self):
        pinecone.init(api_key=self._api_key, environment=self.region)
        self.index = pinecone.Index(self.storage_entity)
        self.describe()

    def describe(self):
        """Describe the index."""
        print(self.index.describe_index_stats())

    def search(self, query: VectorDoc, top_k: int) -> tuple[list, dict, dict]:
        """
        Search the index for similar vectors.

        Args:
            query (VectorDoc): The query vector to search for.
            top_k (int): The number of results to return.

        Returns:
            list[dict]: A list of dictionaries representing the search results.
        """
        query_embedding = query.embedding
        search_result = self.index.query(
            query_embedding, top_k=top_k, include_metadata=True
        )
        return self._prepare_results(search_result)

    def upsert(self, docs: list[VectorDoc]):
        """Insert or update vectors in the index.

        Args:
            docs (list[VectorDoc]): VectorDoc objects to insert or update.
        """
        to_upsert = []
        for doc in docs:
            doc_id, doc_txt, embeddings, metadata = doc.values
            if "text" not in metadata.keys():
                metadata["text"] = doc_txt
            to_upsert.append((doc_id, embeddings, metadata))
        self.index.upsert(vectors=to_upsert)
