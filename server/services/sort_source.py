from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np


class SortSourceService:
    def __init__(self):
        self.embedding_model = SentenceTransformer("all-miniLM-L6-v2")

    def sort_sources(self, query: str, search_results: List[dict]):
        if not search_results:
            print("No search results to sort")
            return []
            
        try:
            relevant_docs = []
            query_embedding = self.embedding_model.encode(query)

            for res in search_results:
                if not res.get("content"):
                    continue
                    
                try:
                    res_embedding = self.embedding_model.encode(res["content"])

                    similarity = float(
                        np.dot(query_embedding, res_embedding)
                        / (np.linalg.norm(query_embedding) * np.linalg.norm(res_embedding))
                    )

                    res["relevance_score"] = similarity

                    if similarity > 0.3:
                        relevant_docs.append(res)
                except Exception as e:
                    print(f"Error processing document: {e}")
                    continue

            return sorted(
                relevant_docs, key=lambda x: x["relevance_score"], reverse=True
            ) if relevant_docs else []
            
        except Exception as e:
            print(f"Error in sort_sources: {e}")
            return []