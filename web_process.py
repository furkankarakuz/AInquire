from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

import warnings
warnings.filterwarnings('ignore')


def news_result(data):
    url = data["target"]

    loader = UnstructuredURLLoader(urls=[url])
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = text_splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(api_key=data["api_key"])
    vectorstore = FAISS.from_documents(documents, embeddings)

    llm = ChatOpenAI(api_key=data["api_key"], model=data["model"], temperature=0)
    qa_chain = RetrievalQA.from_chain_type(llm, chain_type="stuff", retriever=vectorstore.as_retriever())

    result = qa_chain.run(data["question"])
    return result
