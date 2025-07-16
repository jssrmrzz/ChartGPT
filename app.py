from flask import Flask, render_template, request, jsonify
import chromadb
from chromadb.utils.embedding_functions import EmbeddingFunction
from ollama import embeddings
import datetime
import re

app = Flask(__name__)

class OllamaEmbedFunction(EmbeddingFunction):
    def __call__(self, texts):
        vectors = []
        for text in texts:
            try:
                truncated = text[:1000]  # avoid overly long input
                response = embeddings(model="nomic-embed-text", prompt=truncated)
                vector = response["embedding"]
                vectors.append(vector)
            except Exception as e:
                print(f"❌ Embedding failed: {text[:60]}... → {e}")
                vectors.append([0.0] * 768)  # fallback for failed entries
        return vectors

# Initialize ChromaDB client
client = chromadb.PersistentClient(path="./chroma_db")

def get_collection():
    try:
        collection = client.get_collection(
            name="medical_notes",
            embedding_function=OllamaEmbedFunction()
        )
        return collection
    except Exception as e:
        print(f"Error getting collection: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    try:
        query = request.form.get('query', '').strip()
        n_results = int(request.form.get('n_results', 5))
        patient_id = request.form.get('patient_id', '').strip()
        start_date = request.form.get('start_date', '').strip()
        end_date = request.form.get('end_date', '').strip()
        
        if not query:
            return render_template('results.html', 
                                 error="Please enter a search query",
                                 query=query)
        
        collection = get_collection()
        if not collection:
            return render_template('results.html', 
                                 error="Database connection failed",
                                 query=query)
        
        # Build where clause for filtering
        where_clause = {}
        if patient_id:
            where_clause["patient_id"] = {"$eq": patient_id}
        
        # Perform search
        if where_clause:
            results = collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where_clause
            )
        else:
            results = collection.query(
                query_texts=[query],
                n_results=n_results
            )
        
        # Process results
        search_results = []
        if results and results["documents"] and results["documents"][0]:
            for i, (doc, meta, distance) in enumerate(zip(
                results["documents"][0], 
                results["metadatas"][0],
                results["distances"][0] if results["distances"] else [0] * len(results["documents"][0])
            )):
                # Filter by date if specified
                if start_date or end_date:
                    admission_date = meta.get("admission_date", "")
                    if admission_date:
                        try:
                            # Parse date (assuming YYYY-MM-DD format)
                            doc_date = datetime.datetime.strptime(admission_date, "%Y-%m-%d")
                            
                            if start_date:
                                start_dt = datetime.datetime.strptime(start_date, "%Y-%m-%d")
                                if doc_date < start_dt:
                                    continue
                            
                            if end_date:
                                end_dt = datetime.datetime.strptime(end_date, "%Y-%m-%d")
                                if doc_date > end_dt:
                                    continue
                        except ValueError:
                            # Skip if date parsing fails
                            continue
                
                # Calculate similarity score (ChromaDB uses distance, lower is better)
                similarity_score = max(0, 1 - distance) if distance else 0
                
                # Extract key information from document
                doc_preview = doc[:300] + "..." if len(doc) > 300 else doc
                
                # Try to extract diagnosis from document
                diagnosis = "Not specified"
                diagnosis_match = re.search(r"Diagnosis[:\s]*(.*?)(?:\n|$)", doc, re.IGNORECASE)
                if diagnosis_match:
                    diagnosis = diagnosis_match.group(1).strip()
                
                search_results.append({
                    "rank": i + 1,
                    "document": doc_preview,
                    "full_document": doc,
                    "patient_id": meta.get("patient_id", "Unknown"),
                    "admission_date": meta.get("admission_date", "Unknown"),
                    "diagnosis": diagnosis,
                    "similarity_score": round(similarity_score, 3),
                    "distance": round(distance, 3) if distance else 0
                })
        
        return render_template('results.html', 
                             results=search_results,
                             query=query,
                             n_results=n_results,
                             patient_id=patient_id,
                             start_date=start_date,
                             end_date=end_date)
    
    except Exception as e:
        return render_template('results.html', 
                             error=f"Search error: {str(e)}",
                             query=request.form.get('query', ''))

@app.route('/api/search', methods=['POST'])
def api_search():
    """API endpoint for programmatic access"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        n_results = data.get('n_results', 5)
        
        if not query:
            return jsonify({"error": "Query is required"}), 400
        
        collection = get_collection()
        if not collection:
            return jsonify({"error": "Database connection failed"}), 500
        
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        # Format results for API response
        api_results = []
        if results and results["documents"] and results["documents"][0]:
            for doc, meta, distance in zip(
                results["documents"][0], 
                results["metadatas"][0],
                results["distances"][0] if results["distances"] else [0] * len(results["documents"][0])
            ):
                api_results.append({
                    "document": doc,
                    "patient_id": meta.get("patient_id", "Unknown"),
                    "admission_date": meta.get("admission_date", "Unknown"),
                    "similarity_score": round(max(0, 1 - distance), 3),
                    "distance": round(distance, 3) if distance else 0
                })
        
        return jsonify({
            "query": query,
            "results": api_results,
            "total_results": len(api_results)
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stats')
def stats():
    """Display database statistics"""
    try:
        collection = get_collection()
        if not collection:
            return render_template('stats.html', error="Database connection failed")
        
        count = collection.count()
        
        return render_template('stats.html', 
                             total_documents=count,
                             collection_name="medical_notes")
    
    except Exception as e:
        return render_template('stats.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)