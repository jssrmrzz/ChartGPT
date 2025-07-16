# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Workflow

### Process Steps
1. **Analysis & Planning** - Analyze requirements and create detailed plan in `tasks/todo.md`
2. **Plan Verification** - Get approval before starting implementation
3. **Incremental Execution** - Work through todo items one by one
4. **Activity Logging** - Document all actions in `docs/activity.md`
5. **Progress Communication** - Provide high-level summaries of changes
6. **Final Review** - Add summary section to `tasks/todo.md`

### Core Principles
- **Simplicity First** - Minimize code impact and complexity
- **Incremental Progress** - Small, focused changes
- **Clear Communication** - Regular updates and explanations
- **Comprehensive Documentation** - Track all activities and decisions

### File Structure
- `tasks/todo.md` - Current project tasks and completion status
- `docs/activity.md` - Development activity log
- `CLAUDE.md` - Project guidance and workflow (this file)

## Project Overview

This is a medical document search system that uses ChromaDB for vector storage and Ollama for embeddings. The system processes medical notes from CSV files, stores them with embeddings, and provides semantic search capabilities through both command-line and web interfaces.

### Key Components
- **ChromaDB**: Persistent vector database stored in `./chroma_db/`
- **Ollama Integration**: Custom embedding function using `nomic-embed-text` model (768-dimensional vectors)
- **Web Interface**: Flask-based web application with search form and results display
- **Command Line Tools**: Python scripts for data ingestion and querying

## Common Commands

### Web Interface
```bash
# Start the web application
python app.py

# The web interface will be available at http://localhost:5000
```

### Command Line Usage
```bash
# First, embed and store medical notes (if not already done)
python embed_and_store.py

# Query the system from command line
python query_chroma.py
```

### Installation
```bash
# Install required dependencies
pip install -r requirements.txt

# Ensure Ollama is installed and running with nomic-embed-text model
ollama pull nomic-embed-text
```

## Web Interface Features

### Search Functionality
- **Semantic Search**: Uses vector embeddings for intelligent medical document matching
- **Filtering Options**: Filter by patient ID, date range, and number of results
- **Results Display**: Shows similarity scores, patient metadata, and expandable full documents
- **Highlight Matching**: Automatically highlights search terms in results

### API Endpoints
- `POST /search` - Web form search with HTML results
- `POST /api/search` - JSON API for programmatic access
- `GET /stats` - Database statistics and system information

## Data Format

The system expects CSV files with the following columns:
- `medical_report_text` - The medical note content
- `admission_date_lookup` - Patient admission date (YYYY-MM-DD format)
- `patient_id_text` - Patient identifier