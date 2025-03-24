import requests
import os
from dotenv import load_dotenv
from doc_loader import load_document, load_excel, chunk_excel_rows
import chromadb
from chromadb.utils import embedding_functions

load_dotenv()

class OllamaAPI:
    def __init__(self, base_url=None):
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.default_model = os.getenv("DEFAULT_MODEL", "llama3.2")
        
    def generate(self, prompt, model=None, stream=False):
        
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": model or self.default_model,
            "prompt": prompt,
            "stream": stream
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            return None

# Custom Ollama Embedding Function
class OllamaEmbeddingFunction:
    def __init__(self, base_url="http://localhost:11434", model="nomic-embed-text"):
        self.base_url = base_url
        self.model = model

    def __call__(self, input):
        embeddings = []
        for text in input:
            response = requests.post(
                f"{self.base_url}/api/embeddings",
                json={"model": self.model, "prompt": text}
            )
            response.raise_for_status()
            embedding = response.json()["embedding"]
            embeddings.append(embedding)
        return embeddings

def main():
    # Initialize the Ollama API client
    ollama = OllamaAPI()

    # Initialize Chroma client (local)
    chroma_client = chromadb.Client()

    # Initialize embedding function
    ollama_embed = OllamaEmbeddingFunction()

    # Create a Chroma collection with Ollama embedding function
    collection = chroma_client.get_or_create_collection(
        name="my_documents",
        embedding_function=ollama_embed
    )

    # Path to the directory containing your documents
    doc_dir = "docs"

    documents = []
    doc_ids = []

    for filename in os.listdir(doc_dir):
        file_path = os.path.join(doc_dir, filename)
        extension = os.path.splitext(filename)[-1].lower()

        try:
            if extension == ".xlsx":
                chunks, metadatas = load_document(file_path)
                for idx, chunk in enumerate(chunks):
                    documents.append(chunk)
                    doc_ids.append(f"{filename}_row_{idx}")
                collection.add(documents=chunks, ids=doc_ids[-len(chunks):], metadatas=metadatas)
                print(f"✅ Excel file '{filename}' processed into {len(chunks)} row-chunks.")
            else:
                text = load_document(file_path)
                documents.append(text)
                doc_ids.append(filename)
                metadata = {"source": filename}
                collection.add(documents=[text], ids=[filename], metadatas=[metadata])
                print(f"✅ Loaded and indexed document: {filename}")

        except ValueError as e:
            print(f"⚠️ Skipping {filename}: {e}")

    # Add loaded documents to ChromaDB
    collection.add(documents=documents, ids=doc_ids)

    # Example query
    query = "Stöder systemet API-integration?"

    results = collection.query(
        query_texts=[query],
        n_results=2
    )

    print("\n🔎 Documents most relevant to your query:")
    for doc, doc_id in zip(results["documents"][0], results["ids"][0]):
        print(f"\n📄 Document ID: {doc_id}\nContent snippet: {doc[:500]}...")

    # AI-generated response based on retrieved context
    context = "\n---\n".join(results["documents"][0])
    prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer concisely based on the context."

    ai_response = ollama.generate(prompt)

    if ai_response:
        print("\n✨ AI-enhanced response:")
        print(ai_response['response'])

if __name__ == "__main__":
    main()
