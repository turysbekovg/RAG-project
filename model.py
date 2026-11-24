import sys
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQAWithSourcesChain
from langchain_openai import OpenAI
import os
#import shutil

openai_api_key = 'SOME_KEY'

categories = ['aerospace', 'automotive', 'biomedical']
base_path = 'datasets'
persist_directory = "chroma"

# Function to create a vectore store
def create_or_load_vector_store(categories):
    
    vector_store_directory = os.path.join(persist_directory, "all_categories")
    
    # If the vector store already exists, then load it
    if os.path.exists(vector_store_directory): 
        print("Loading existing vector store for all categories")
        vectordb = Chroma(
            persist_directory=vector_store_directory,
            embedding_function=OpenAIEmbeddings(openai_api_key=openai_api_key)
        )
    else: # create new vector store
        print("Creating new vector store for all categories")
        all_documents = []

        # collect all documents from every field
        for category in categories:
            pdf_folder_path = os.path.join(base_path, f"{category}_new") 
            documents = []

            for file in os.listdir(pdf_folder_path): # going through each PDF 
                if file.endswith('.pdf'):
                    try:
                        pdf_path = os.path.join(pdf_folder_path, file)
                        loader = PyPDFLoader(pdf_path)
                        documents.extend(loader.load())
                    except Exception as e:
                        print(f"Error loading {file}: {e}")

            all_documents.extend(documents) # new list to combine all documents to one list, which will then be converted to vectors

        print(f"Total number of documents across all categories: {len(all_documents)}")

        # Devision to chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
        chunked_documents = text_splitter.split_documents(all_documents)

        # Creating vector store from chunked documents
        vectordb = Chroma.from_documents(
            documents=chunked_documents,
            embedding=OpenAIEmbeddings(openai_api_key=openai_api_key),
            persist_directory=vector_store_directory
        )
        vectordb.persist()

    print("Creating or Loading the database is done.")

    return vectordb

vector_stores = create_or_load_vector_store(categories) # create ChromaDB

# Defining the model
llm = OpenAI(model_name="gpt-3.5-turbo-instruct", temperature=0, openai_api_key=openai_api_key)

# function that will generate responses
def generate_response(query, vector_stores, top_k=6): 

    print("Generating response...")

    retriever = vector_stores.as_retriever(top_k=top_k)
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm=llm, chain_type="stuff", retriever=retriever)
    result = chain({"question": query})

    sources = result['sources'].split(', ')  # Assuming sources are separated by commas
    formatted_sources = "\n".join([f"{i+1}) {source}" for i, source in enumerate(sources)])
    response = f"{result['answer']}\nSources:\n{formatted_sources}\n"

    return response

# Main function
if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "What are the industry standards or regulations related to using titanium alloy or stainless steels or aluminum alloy in additive manufacturing"
    response = generate_response(query, vector_stores, top_k=6)
    print(response)
