import os
import pickle
import tempfile
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings import FakeEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class Embedder:

    def __init__(self):
        self.PATH = "embeddings"
        self.mkEmbeddingsDirectory()

    def mkEmbeddingsDirectory(self):
        """
        Creates a directory to store the embeddings vectors
        """
        if not os.path.exists(self.PATH):
            os.mkdir(self.PATH)

    def storeDocumentEmbeddings(self, file, original_filename):
        """
        Stores document embeddings using Langchain and FAISS
        """
        embeddings = None
        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as tmp_file:
            tmp_file.write(file)
            tmp_file_path = tmp_file.name
            
        def get_file_extension(uploaded_file):
            file_extension =  os.path.splitext(uploaded_file)[1].lower()
            
            return file_extension
        
        text_splitter = RecursiveCharacterTextSplitter(
                chunk_size = 7000,
                chunk_overlap  = 100,
                length_function = len,
            )
        loader = TextLoader(file_path=tmp_file_path, encoding="utf-8")
        data = loader.load_and_split(text_splitter)
            
            
        # embeddings = OpenAIEmbeddings()

        # embeddings = FakeEmbeddings(size=4000)
            
        try: 
            embeddings = OpenAIEmbeddings()
            vectors = FAISS.from_documents(data, embeddings)
        except:
            embeddings = FakeEmbeddings(size=4000)
            vectors = FAISS.from_documents(data, embeddings)
        os.remove(tmp_file_path)

        # Save the vectors to a pickle file
        with open(f"{self.PATH}/{original_filename}.pkl", "wb") as f:
            pickle.dump(vectors, f)

    def retrieveDocumentEmbeddings(self, file, original_filename):
        """
        Retrieves document embeddings
        """
        if not os.path.isfile(f"{self.PATH}/{original_filename}.pkl"):
            self.storeDocumentEmbeddings(file, original_filename)

        # Load the vectors from the pickle file
        with open(f"{self.PATH}/{original_filename}.pkl", "rb") as f:
            vectors = pickle.load(f)
        
        return vectors
