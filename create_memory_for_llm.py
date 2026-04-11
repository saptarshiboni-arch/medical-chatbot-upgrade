from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

## Uncomment the following files if you're not using pipenv as your virtual environment manager
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


# Step 1: Load raw PDF(s)
DATA_PATH="data/"
def load_pdf_files(data):
    loader = DirectoryLoader(data,
                             glob='*.pdf',
                             loader_cls=PyPDFLoader)
    
    documents=loader.load()
    return documents

documents=load_pdf_files(data=DATA_PATH)
#print("Length of PDF pages: ", len(documents))


# Step 2: Create Chunks
def create_chunks(extracted_data):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=500,
                                                 chunk_overlap=50)
    text_chunks=text_splitter.split_documents(extracted_data)
    return text_chunks

text_chunks=create_chunks(extracted_data=documents)
#print("Length of Text Chunks: ", len(text_chunks))

# Step 3: Create Vector Embeddings 

def get_embedding_model():
    embedding_model=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embedding_model

embedding_model=get_embedding_model()


# --- STEP 4: Store embeddings in FAISS (Safe Batch Mode) ---
DB_FAISS_PATH = "vectorstore/db_faiss"

# Start with the first 50 chunks to initialize the database
print(f"Total chunks to process: {len(text_chunks)}")
print("Processing first batch...")
db = FAISS.from_documents(text_chunks[:50], embedding_model)

# Process the rest in batches of 50
batch_size = 50
for i in range(50, len(text_chunks), batch_size):
    batch = text_chunks[i : i + batch_size]
    db.add_documents(batch)
    print(f"Successfully indexed up to chunk {i + len(batch)}...")
    
    # Save progress to disk every 200 chunks so you don't lose work
    if i % 200 == 0:
        db.save_local(DB_FAISS_PATH)
        print("--- Progress saved to disk ---")

# Final Save
db.save_local(DB_FAISS_PATH)
print("Success! All 759 pages are now in your vector memory.")