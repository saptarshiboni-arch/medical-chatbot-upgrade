import os


from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain import hub
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain


## Uncomment the following files if you're not using pipenv as your virtual environment manager
from dotenv import load_dotenv
load_dotenv()


DB_FAISS_PATH="vectorstore/db_faiss"

def get_vectorstore():
    embedding_model=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    db=FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)
    return db

print("Loading vectorstore from disk...")
vectorstore = get_vectorstore()
print("Vectorstore loaded successfully.")

def get_response(user_query):
    try:
        GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.5,
            max_tokens=512,
            api_key=GROQ_API_KEY,
        )

        retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

        combine_docs_chain = create_stuff_documents_chain(
            llm,
            retrieval_qa_chat_prompt
        )

        rag_chain = create_retrieval_chain(
            vectorstore.as_retriever(search_kwargs={'k': 3}),
            combine_docs_chain
        )

        response = rag_chain.invoke({'input': user_query})

        return response["answer"]

    except Exception as e:
        return str(e)






