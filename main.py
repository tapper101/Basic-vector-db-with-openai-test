import requests
import os
import openai
from dotenv import load_dotenv
from doc_loader import load_document
import chromadb
from chromadb.utils import embedding_functions

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

class OpenAIAPI:
    def __init__(self, model=None):
        self.default_model = model or os.getenv("DEFAULT_CHATGPT_MODEL", "gpt-3.5-turbo")

    def generate(self, prompt, model=None):
        try:
            response = openai.ChatCompletion.create(
                model=model or self.default_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
            )
            return response.choices[0].message.content.strip()
        except openai.OpenAIError as e:
            print(f"OpenAI API error: {e}")
            return None

class OpenAIEmbeddingFunction:
    def __init__(self, model=None):
        self.embedding_model = model or os.getenv("DEFAULT_EMBEDDING_MODEL", "text-embedding-3-small")

    def __call__(self, input):
        try:
            response = openai.Embedding.create(
                input=input,
                model=self.embedding_model
            )
            embeddings = [data["embedding"] for data in response["data"]]
            print("✅ Embedding success.")
            return embeddings
        except openai.OpenAIError as e:
            print(f"OpenAI Embedding API error: {e}")
            return []

def main():
    # Initialize OpenAI API client
    openai_client = OpenAIAPI()

    # Initialize Chroma client (local)
    chroma_client = chromadb.Client()

    # Initialize OpenAI embedding function
    openai_embed = OpenAIEmbeddingFunction()

    # Create a Chroma collection with OpenAI embedding function
    collection = chroma_client.get_or_create_collection(
        name="my_documents",
        embedding_function=openai_embed
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
                # ✅ Extract the text to embed and the full document text
                # Use the left side of the pipe for embedding (query-relevant)
                embedding_inputs = [chunk["embed"] for chunk in chunks]

                # Use the full row (left | right) for context
                full_contents = [chunk["full"] for chunk in chunks]

                # Generate unique IDs
                new_ids = [f"{filename}_row_{idx}" for idx in range(len(chunks))]

                # ✅ Generate embeddings from the 'embed' side only
                embeddings = openai_embed(embedding_inputs)

                # ✅ Store full content + correct embeddings
                collection.add(
                    documents=full_contents,
                    embeddings=embeddings,
                    ids=new_ids,
                    metadatas=metadatas
                )

                print(f"✅ Excel file '{filename}' processed into {len(chunks)} row-chunks.")
                print(f"🧾 Sample chunk: {chunks[0] if chunks else 'No content'}")

                
            else:
                text = load_document(file_path)
                documents.append(text)
                doc_ids.append(filename)
                metadata = {"source": filename}
                collection.add(documents=[text], ids=[filename], metadatas=[metadata])
                print(f"✅ Loaded and indexed document: {filename}")

        except ValueError as e:
            print(f"⚠️ Skipping {filename}: {e}")

    # Example query
    query = "Går det att välja att matcha artikel i faktura mot viss artikel i order (t.ex. då leverantör bytt artikelnummer)?"

    results = collection.query(
        query_texts=[query],
        n_results=2,
        include=["documents", "metadatas", "distances"]
    )

    # Filter results: only include documents within a good distance threshold
    DISTANCE_THRESHOLD = 0.5  # adjust as needed: lower = more strict

    filtered_docs = []
    filtered_ids = []
    filtered_metadata = []

    for doc, doc_id, meta, distance in zip(
        results["documents"][0],
        results["ids"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        if distance <= DISTANCE_THRESHOLD:
            filtered_docs.append(doc)
            filtered_ids.append(doc_id)
            filtered_metadata.append(meta)

    print(f"\n🔍 Query: {query}")

    if filtered_docs:
        print("\n🔎 Highly relevant documents:")
        for doc, doc_id, metadata in zip(filtered_docs, filtered_ids, filtered_metadata):
            print(f"\n📄 Document ID: {doc_id}")
            print(f"📏 Similarity distance: {distance:.4f}")
            print(f"📎 Metadata: {metadata}")
            print(f"📄 Content snippet: {doc[:1000]}...")

        # Build LLM prompt from top-matching filtered chunks
        context = "\n---\n".join(filtered_docs)
        
        prompt = f"""You are a helpful assistant.

        Context:
        {context}

        Question:
        {query}

        Instructions:
        Answer concisely based only on the context. In the context, values appearing after the '|' character are to be used to determine a positive or negative answer. For example, 'J' means yes and 'N' means no. Answer in Swedish, with 'Ja' or 'Nej'"""

        
        ai_response = openai_client.generate(prompt)

        if ai_response:
            print("\n✨ AI-enhanced response:")
            print(ai_response)
    else:
        print("⚠️ No documents matched closely enough to generate a reliable answer.")


if __name__ == "__main__":
    main()
