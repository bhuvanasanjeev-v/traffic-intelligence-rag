from app.query_rewrite.rewriter import rewrite_query
# from app.reranker.reranker import rerank_documents
from app.retrieval.bm25_retriever import bm25_search
from app.retrieval.hybrid_retriever import hybrid_retrieve
from app.retrieval.retriever import retrieve_documents
from app.utils.context_builder import build_context
from app.utils.generate_answer import generate_answer
from app.utils.prompt_builder import build_prompt
from app.utils.source_utils import get_sources


class RAGPipeline:
    """Orchestrates retrieval, reranking, prompting, and answer generation."""

    def __init__(
        self,
        documents,
        embed_fn=None,
        answer_fn=generate_answer,
        prompt_name="rag_answer_prompt.txt",
        default_filters=None,
        faiss_top_k=5,
        bm25_top_k=5,
        hybrid_top_k=5,
        rerank_top_k=3,
        enable_query_rewrite=True,
        chat_history=None,
    ):
        self.documents = documents
        self.embed_fn = embed_fn or self._default_embed_fn()
        self.answer_fn = answer_fn
        self.prompt_name = prompt_name
        self.default_filters = default_filters
        self.faiss_top_k = faiss_top_k
        self.bm25_top_k = bm25_top_k
        self.hybrid_top_k = hybrid_top_k
        self.rerank_top_k = rerank_top_k
        self.enable_query_rewrite = enable_query_rewrite
        self.chat_history = chat_history or []

    def _default_embed_fn(self):
        from app.embeddings.embedder import generate_embeddings

        return generate_embeddings

    def ask(self, query, filters=None):
        active_filters = self.default_filters if filters is None else filters
        rewritten_query = self._rewrite_query(query)

        faiss_docs = retrieve_documents(
            query=rewritten_query,
            documents=self.documents,
            embed_fn=self.embed_fn,
            top_k=self.faiss_top_k,
            filters=active_filters,
        )

        bm25_docs = bm25_search(
            query=rewritten_query,
            documents=self.documents,
            top_k=self.bm25_top_k,
            filters=active_filters,
        )

        candidate_docs = hybrid_retrieve(
            query=rewritten_query,
            faiss_docs=faiss_docs,
            bm25_docs=bm25_docs,
            top_k=self.hybrid_top_k,
        )

        # reranked_docs = rerank_documents(
        #     query=rewritten_query,
        #     documents=candidate_docs,
        #     top_k=self.rerank_top_k,
        # )

        reranked_docs = candidate_docs[:3]

        context = build_context(reranked_docs)

        prompt = build_prompt(
            self.prompt_name,
            context,
            rewritten_query,
        )

        answer = self.answer_fn(prompt)
        sources = get_sources(reranked_docs)
        self._update_chat_history(query, answer)

        return {
            "answer": answer,
            "sources": sources,
            "retrieved_docs": reranked_docs,
            "context": context,
            "query": query,
            "rewritten_query": rewritten_query,
        }

    def _rewrite_query(self, query):
        if not self.enable_query_rewrite:
            return query

        return rewrite_query(
            current_query=query,
            chat_history=self.chat_history,
            answer_fn=self.answer_fn,
        )

    def _update_chat_history(self, query, answer):
        self.chat_history.append(
            {
                "role": "user",
                "content": query,
            }
        )

        self.chat_history.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )
