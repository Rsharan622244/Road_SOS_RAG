"""
rag_engine.py - RAG pipeline for RoadSoS first-aid chatbot

CONCEPT:
  Text files -> chunks -> Gemini embeddings -> FAISS index (saved to disk)
  Question -> embed -> find similar chunks -> Gemini answers using those chunks

This is Retrieval-Augmented Generation (RAG):
- We don't fine-tune the model (expensive)
- We retrieve relevant text at query time and inject into the prompt (cheap, fast)
"""
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_huggingface import HuggingFaceEmbeddings


load_dotenv()

VECTORSTORE_PATH = "vectorstore/faiss_index"
KNOWLEDGE_BASE_PATH = "knowledge_base"
GEMINI_KEY = os.getenv("GEMINI_API_KEY")


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def build_vectorstore():
    """
    Loads all .txt files from knowledge_base/,
    splits into chunks, embeds with Gemini, saves FAISS index.
    Run once — after that load_vectorstore() is used. 
    """
    print("[RAG] Loading knowledge base files...")

    from langchain_core.documents import Document
    from langchain_community.document_loaders import TextLoader
    import glob

    def safe_load_file(filepath):
        for enc in ["utf-8", "cp1252", "latin-1", "ascii"]:
            try:
                loader = TextLoader(filepath, encoding=enc)
                return loader.load()
            except Exception:
                continue

        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        return [Document(page_content=content, metadata={"source": filepath})]


    docs = []

    for filepath in glob.glob(f"{KNOWLEDGE_BASE_PATH}/**/*.txt", recursive=True):
        docs.extend(safe_load_file(filepath))

    # loader = DirectoryLoader(
    #     KNOWLEDGE_BASE_PATH,
    #     glob="**/*.txt",
    #     loader_cls=TextLoader,
    #     loader_kwargs={"encoding": "utf-8"}
    # )
    # docs = loader.load()
    print(f"[RAG] Loaded {len(docs)} documents")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=["\n\n", "\n", ". ", " "]
    )
    chunks = splitter.split_documents(docs)
    print(f"[RAG] Split into {len(chunks)} chunks")

    print("[RAG] Building embeddings (this takes ~30 seconds)...")
    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)

    os.makedirs("vectorstore", exist_ok=True)
    vectorstore.save_local(VECTORSTORE_PATH)
    print(f"[RAG] Vector store saved to {VECTORSTORE_PATH}")
    return vectorstore


def load_vectorstore():
    """Load existing FAISS index from disk."""
    if not os.path.exists(VECTORSTORE_PATH):
        return None
    embeddings = get_embeddings()
    return FAISS.load_local(
        VECTORSTORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )


def get_or_build_vectorstore():
    """Load if exists, build if not."""
    vs = load_vectorstore()
    if vs:
        print("[RAG] Loaded existing vector store")
        return vs
    print("[RAG] No vector store found — building now...")
    return build_vectorstore()


def build_qa_chain(vectorstore):
    """
    Creates a ConversationalRetrievalChain:
    - Retriever: finds top 4 relevant chunks from FAISS
    - Memory: remembers last 5 chat turns for follow-up questions
    - LLM: Gemini answers using retrieved chunks as context
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=GEMINI_KEY,
        temperature=0.2,
        # convert_system_message_to_human=True
    )

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""You are RoadSoS, an AI first-aid assistant for road accident emergencies.
Answer ONLY using the context below. Be clear, calm, and practical.
If the answer is not in the context, say: "Please call 112 immediately for professional help."
Never give advice that could worsen injuries.

Context:
{context}

Question: {question}

Answer (be concise and numbered if giving steps):"""
    )

    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": prompt},
        return_source_documents=True,
        verbose=False
    )


def ask(qa_chain, question: str) -> dict:
    """Run one Q&A turn. Returns answer + source file names."""
    result = qa_chain.invoke({"question": question})

    sources = list({
        os.path.basename(doc.metadata.get("source", ""))
        for doc in result.get("source_documents", [])
    })

    return {
        "answer": result["answer"],
        "sources": sources
    }


# Global QA chain — loaded once, reused for all requests
_qa_chain = None

def get_qa_chain():
    global _qa_chain
    if _qa_chain is None:
        vs = get_or_build_vectorstore()
        _qa_chain = build_qa_chain(vs)
    return _qa_chain