from typing import Any, Callable, Dict, List, Optional, Tuple

from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.base import Embeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from ...integrations.langchain import SeaplaneLLM, langchain_vectorstore, seaplane_embeddings
from ...logging import log
from ...model.vector import Vector
from ...vector import vector_store


class Store:
    def __init__(self, index: str) -> None:
        self.index = index
        self.chat_history_file: Dict[str, List[Tuple[str, str]]] = {}
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            length_function=len,
            add_start_index=True,
        )

    def save(
        self, file_name: str, file_url: str, embeddings: Embeddings = seaplane_embeddings
    ) -> None:
        loader = PyPDFLoader(file_url)
        pages = loader.load_and_split()
        texts = self.text_splitter.split_documents(pages)

        embed_vectors = embeddings.embed_documents([page.page_content for page in texts])
        vectors = [
            Vector(
                vector=vector,
                metadata={
                    "page_content": texts[idx].page_content,
                    "metadata": texts[idx].metadata,
                },
            )
            for idx, vector in enumerate(embed_vectors)
        ]

        result = vector_store.insert(self.index, vectors)
        log.info(f"⏳ Saving file {file_name}: {result}")

    def query(
        self, file_name: str, query: str, embeddings: Embeddings = seaplane_embeddings
    ) -> Dict[str, Any]:
        vectorstore = langchain_vectorstore(self.index, embeddings)

        qa = ConversationalRetrievalChain.from_llm(
            llm=SeaplaneLLM(),
            retriever=vectorstore.as_retriever(),
            return_source_documents=True,
        )

        history = self.chat_history_file.get(file_name, None)
        if history is None:
            history = []
            self.chat_history_file[file_name] = []

        result = qa({"question": query, "chat_history": history})
        self.chat_history_file[file_name].append((query, result["answer"]))

        return {"answer": result["answer"], "history": history}


class VectorDbTask:
    def __init__(self, func: Callable[[Any], Any], id: str, model: Optional[str]) -> None:
        self.func = func
        self.args: Optional[Tuple[Any, ...]] = None
        self.kwargs: Optional[Dict[str, Any]] = None
        self.type = "vectordb"
        self.model = model
        self.id = id

    def process(self, *args: Any, **kwargs: Any) -> Any:
        self.args = args
        self.kwargs = kwargs

        if self.type == "vectordb":
            log.info("Accessing Vector DB task...")
            # self.args = self.args + (Store(),)

            return self.func(*self.args, **self.kwargs)

    def print(self) -> None:
        log.info(f"id: {self.id}, type: {self.type}, model: {self.model}")
