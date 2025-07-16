<pre>
 .d8888b.  888                       888     .d8888b.  8888888b. 88888888888 
d88P  Y88b 888                       888    d88P  Y88b 888   Y88b    888     
888    888 888                       888    888    888 888    888    888     
888        88888b.   8888b.  888d888 888888 888        888   d88P    888     
888        888 "88b     "88b 888P"   888    888  88888 8888888P"     888     
888    888 888  888 .d888888 888     888    888    888 888           888     
Y88b  d88P 888  888 888  888 888     Y88b.  Y88b  d88P 888           888     
 "Y8888P"  888  888 "Y888888 888      "Y888  "Y8888P88 888           888     
                                                                             
</pre>                                                                           
                                                                             
⸻

🧠 Semantic Search over Medical Notes (with Embeddings & Vector DB)

This project enables semantic search across medical notes by embedding both clinical notes and user queries into a vector space, storing them in ChromaDB, and retrieving the most relevant matches.

⸻

🔧 Data Preparation & Embedding (embed_and_store.py)
	•	Loads a CSV file of cleaned medical notes.
	•	Uses the Ollama API to generate vector embeddings for each note.
(Long texts are truncated for efficiency.)
	•	Stores the embeddings and metadata (e.g., patient_id, admission_date) in a persistent Chroma vector database.

⸻

🔍 Querying the Notes (query_chroma.py)
	•	Loads the same embedding function and connects to the Chroma database.
	•	Accepts a user query, embeds it, and retrieves the most semantically similar medical notes.
	•	Displays the top matches along with their metadata.

⸻

▶️ How to Run

💡 Make sure you have Python 3.10+ and Ollama installed and running locally.

1. Install Dependencies

pip install -r requirements.txt

2. Start the Ollama Model

Make sure your local model is running:

ollama run <your-embedding-model>

Replace <your-embedding-model> with the name of the model you’re using (e.g., nomic-embed-text or barbershop-rev).

3. Embed and Store Notes

Run this script to load your CSV, embed notes, and store them:

python embed_and_store.py

The script assumes a CSV with columns like note_text, patient_id, admission_date.

4. Run Semantic Search

Search similar notes using a natural language query:

python query_chroma.py

You’ll be prompted to enter your query (e.g., "shortness of breath after surgery"), and the most relevant notes will be displayed.

⸻

✅ Summary

This project allows for:
* Fast and meaningful search of clinical notes.
* Finding similar cases or relevant context in large collections of medical records.
* A foundation for building intelligent medical search assistants or decision-support tools.
* Dataset used: https://www.kaggle.com/datasets/ihssanened/mimic-iii-clinical-databaseopen-access/data

⸻

🤖 What is Embedding?

Embedding is the process of turning text (like a medical note or user question) into a vector — a list of numbers that captures the meaning of the text.

For example:
	•	"chest pain" → [0.12, -0.34, 0.98, ...]
	•	"heart discomfort" → [0.11, -0.33, 0.97, ...]

Even though the words are different, the embeddings are close together because the meanings are similar. This is what allows semantic search — finding things based on meaning, not just exact words.

⸻

📦 Why Use a Vector Database?

A vector database (like ChromaDB) is designed to:
*	Store these embeddings alongside metadata (like patient ID or date)
*	Quickly search for the most similar vectors (using methods like cosine similarity)

In this project, we:
*	Embed all medical notes into vectors and store them
*	Embed a user query the same way
*	Use the vector DB to find notes with similar embeddings, i.e., similar meaning

Without a vector database, comparing the query to thousands of notes would be very slow and inefficient.
