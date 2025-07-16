import chromadb
from chromadb.utils.embedding_functions import EmbeddingFunction
from ollama import embeddings

# Use same embedding class
class OllamaEmbedFunction(EmbeddingFunction):
    def __call__(self, texts):
        return [embeddings(model="nomic-embed-text", prompt=text)["embedding"] for text in texts]

# Initialize Chroma client
#client = chromadb.Client()
client = chromadb.PersistentClient(path="./chroma_db") #persistent storage
collection = client.get_collection(
    name="medical_notes",
    embedding_function=OllamaEmbedFunction()
)

# Sample user query
query = "patient with lung cancer and low hemoglobin"
results = collection.query(
    query_texts=[query],
    n_results=3
)

# Show results
for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    print("📝 Match:", doc[:150])
    print("📅 Admission Date:", meta["admission_date"])
    print("🧍 Patient ID:", meta["patient_id"])
    print("---")