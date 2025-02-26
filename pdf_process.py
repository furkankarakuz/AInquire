from langchain.schema import Document
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

import fitz
import os
import shutil
import warnings

warnings.filterwarnings('ignore')


def delete_files():
    static_dir = "static"
    if os.path.exists(static_dir):
        for file in os.listdir(static_dir):
            file_path = os.path.join(static_dir, file)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"File Error:{str(e)}")


def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def answer_question_from_pdf(data):
    pdf_file = data["target"]
    pdf_text = extract_text_from_pdf(pdf_file)
    delete_files()
    if pdf_text:
        documents = [Document(page_content=pdf_text, metadata={"source": "pdf"})]
        embeddings = OpenAIEmbeddings(api_key=data["api_key"])
        vectorstore = FAISS.from_documents(documents, embeddings)
        llm = ChatOpenAI(api_key=data["api_key"], model=data["model"], temperature=0)
        qa_chain = RetrievalQA.from_chain_type(llm, retriever=vectorstore.as_retriever())
        answer = qa_chain.run(data["question"])
        return answer
    else:
        return "Could not extract text from PDF."
