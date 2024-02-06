from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader


class EmbeddingsProvider:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingsProvider, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        self.initialized = False
        self.embedding_model_name = "mrm8488/distiluse-base-multilingual-cased-v2-finetuned-stsb_multi_mt-es"
        self.file_path = "communist_manifest.pdf"
        self.documents = self.load_documents(self.file_path)
        self.embeddings, self.knowledge_base = self.create_embeddings(self.embedding_model_name, self.documents)
        self.initialized = True

    def load_documents(self, file_path):
        loader = PyPDFLoader(file_path)
        return loader.load_and_split()
    

    def create_embeddings(self, model_name, documents):
        embeddings = HuggingFaceEmbeddings(model_name=model_name)

            
        knowledge_base = FAISS.from_documents(documents, embeddings)
        return embeddings, knowledge_base
    def get_embeddings(self):
        return self.embeddings, self.knowledge_base


