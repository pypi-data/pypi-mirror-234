# Implementación de un chatbot que se alimenta a partir docx, pdf y txt
import os
import inspect
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyMuPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate # noqa


class Chatbot:

    def __init__(self, openai_api_key, model, search_kwargs): # noqa
        self.vectorstore = None
        self.chain = None
        self.openai_api_key = openai_api_key
        self.model = model
        self.search_kwargs = search_kwargs

    def vector_store_local(self, persist=False):

        if persist:
            documents = []
            frame = inspect.currentframe()
            caller_file = inspect.getouterframes(frame)[-1].filename
            basedir = os.path.dirname(os.path.abspath(caller_file))
            docsdir = os.path.join(basedir, "documents")

            if not os.path.exists(docsdir):
                print("No documents directory found")
                return

            for file_name in os.listdir(docsdir):
                file_path = os.path.join(docsdir, file_name)
                if file_name.endswith(".pdf"):
                    loader = PyPDFLoader(file_path)
                    documents.extend(loader.load())
                elif file_name.endswith(".docx") or file_name.endswith(".doc"):
                    loader = Docx2txtLoader(file_path)
                    documents.extend(loader.load())
                elif file_name.endswith(".txt"):
                    loader = TextLoader(file_path)
                    documents.extend(loader.load())

            text_splitter = CharacterTextSplitter(
                chunk_size=800, chunk_overlap=200
            )

            documents = text_splitter.split_documents(documents)

            self.vectorstore = Chroma.from_documents(
                documents, embedding=OpenAIEmbeddings(
                    openai_api_key=self.openai_api_key
                ),
                persist_directory=f"{basedir}/vs_data"
            )

            self.vectorstore.persist()
        else:
            embeddings = OpenAIEmbeddings(
                openai_api_key=self.openai_api_key
            )
            self.vectorstore = Chroma(
                persist_directory=f"{basedir}/vs_data",
                embedding_function=embeddings
            )

    def vector_store_online(self, url):
        loader = PyMuPDFLoader(url)
        documents = loader.load()

        text_splitter = CharacterTextSplitter(
            chunk_size=800, chunk_overlap=200
        )

        documents = text_splitter.split_documents(documents)

        self.vectorstore = Chroma.from_documents(
            documents, embedding=OpenAIEmbeddings(),
            persist_directory="vs_data"
        )

        self.vectorstore.persist()

    def load_chain(self):

        if self.vectorstore is None:
            return

        general_system_template = r"""
        Dado el context, eres experto en analizar distintos mensajes de texto
        y sacar conclusiones muy acertadas.
        ----
        {context}
        ----

        """
        general_user_template = "Question:{question}"

        messages = [
            SystemMessagePromptTemplate.from_template(general_system_template),
            HumanMessagePromptTemplate.from_template(general_user_template)
        ]

        qa_prompt = ChatPromptTemplate.from_messages(messages)

        self.chain = ConversationalRetrievalChain.from_llm(
            ChatOpenAI(temperature=0.3, model_name=self.model, openai_api_key=self.openai_api_key), # noqa
            self.vectorstore.as_retriever(search_kwargs={'k': self.search_kwargs}), # noqa
            combine_docs_chain_kwargs={"prompt": qa_prompt}, # noqa
            return_source_documents=False,
            verbose=False,
        )

    def get_chatbot_answer(self, question, chat_history=[]):

        '''returns a dict with the answer and the chat history'''
        return self.chain({
            "question": question, "chat_history": chat_history
        })
