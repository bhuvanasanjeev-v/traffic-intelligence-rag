# MODEL_NAME = "BAAI/bge-reranker-base"
# _model = None


# def get_reranker_model():
#     global _model

#     if _model is None:
#         from sentence_transformers import CrossEncoder

#         _model = CrossEncoder(MODEL_NAME)

#     return _model


# def rerank_documents(
#         query,
#         documents,
#         top_k=3):

#     if not documents:
#         return []

#     model = get_reranker_model()

#     pairs = [
#         (query, doc["text"])
#         for doc in documents
#     ]

#     scores = model.predict(pairs)

#     ranked = sorted(
#         zip(documents, scores),
#         key=lambda x: x[1],
#         reverse=True
#     )

#     reranked_docs = []

#     for doc, score in ranked[:top_k]:
#         reranked_doc = doc.copy()
#         reranked_doc["rerank_score"] = float(score)
#         reranked_docs.append(reranked_doc)

#     return reranked_docs
