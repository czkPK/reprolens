from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


def build_agent():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2, max_tokens=512)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    docs = ["ReproLens audits open-source LLM projects."]
    vector_store = FAISS.from_texts(docs, embeddings)
    retriever = vector_store.as_retriever()
    return llm, retriever


def main():
    llm, retriever = build_agent()
    query = "What does ReproLens audit?"
    context = "\n".join(doc.page_content for doc in retriever.invoke(query))
    response = llm.invoke(f"Context:\n{context}\n\nQuestion: {query}")
    print(response.content)


if __name__ == "__main__":
    main()
