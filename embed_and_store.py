import pandas as pd
import chromadb
from chromadb.utils.embedding_functions import EmbeddingFunction
from ollama import embeddings  # ✅ new import

# Load cleaned data
df = pd.read_csv("cleaned_medical_notes.csv")

# Optional: Rename columns if needed
df.rename(columns={
    "medical_report_text": "text",
    "admission_date_lookup": "admission_date",
    "patient_id_text": "patient_id"
}, inplace=True)

# Step 1: Define embedding function using Ollama Python API
class OllamaEmbedFunction(EmbeddingFunction):
    def __call__(self, texts):
        vectors = []
        for text in texts:
            try:
                truncated = text[:1000]  # avoid overly long input
                print("🔍 Embedding input:", truncated[:100].replace("\n", " ") + "...")
                
                response = embeddings(model="nomic-embed-text", prompt=truncated)
                vector = response["embedding"]
                vectors.append(vector)

            except Exception as e:
                print(f"❌ Embedding failed: {text[:60]}... → {e}")
                vectors.append([0.0] * 768)  # fallback for failed entries
        return vectors

# Step 2: Initialize Chroma DB
#client = chromadb.Client()
client = chromadb.PersistentClient(path="./chroma_db")  # persistent storage
collection = client.get_or_create_collection(
    name="medical_notes",
    embedding_function=OllamaEmbedFunction()
)

# Step 3: Add records to Chroma
for i, row in df.iterrows():
    collection.add(
        documents=[str(row.get("text", ""))],
        metadatas=[{
            "patient_id": str(row.get("patient_id", "unknown")),
            "admission_date": str(row.get("admission_date", ""))
        }],
        ids=[f"record-{i}"]
    )

print("✅ All records embedded and stored in Chroma!")