# Project Tasks

## Project Setup
- [x] Initialize project structure (directories, basic files)
- [x] Setup `pyproject.toml` with `uv` - *File exists.*
- [x] **Review existing Python files (`main.py`, `extract_classes.py`) and integrate or remove.** - *Removed `main.py`. Kept `extract_classes.py` as reference for parser/chunker implementation.*
- [x] Add initial dependencies (`llama-index`, `chromadb`, `openai`, `streamlit`, `lxml`) using `uv add`
- [x] Initial commit - *Done as part of adding dependencies.*

## 1. Doxygen Parser
- [x] Identify target Doxygen XML files/structure (`data/llvm-project/output/xml/`)
- [x] Define data structure(s) for extracted code elements (functions, classes, etc.) (`src/codiculum/doxygen_parser/models.py`)
- [x] Implement XML parsing logic using `lxml` or `xml.etree.ElementTree`
- [ ] Extract relevant information (signatures, docstrings, locations)
- [ ] Add error handling for parsing

## 2. Code Chunker
- [ ] Define chunking strategy (e.g., by function, class)
- [ ] Implement chunking logic based on parsed Doxygen data
- [ ] Consider source code retrieval if needed for full context

## 3. Embedding Generator
- [ ] Configure OpenAI embedding model via LlamaIndex settings
- [ ] Implement function to generate embeddings for code chunks
- [ ] Handle potential API errors

## 4. Vector Store Manager (ChromaDB)
- [ ] Initialize ChromaDB client (local persistence)
- [ ] Configure LlamaIndex `ChromaVectorStore`
- [ ] Implement logic to add/update embedded chunks in ChromaDB
- [ ] Implement logic to load existing store

## 5. RAG Pipeline (LlamaIndex)
- [ ] Construct LlamaIndex `VectorStoreIndex` from ChromaDB store
- [ ] Configure query engine (retriever, response synthesizer)
- [ ] Implement query function

## 6. Streamlit UI
- [ ] Create basic Streamlit app file (`app.py`)
- [ ] Add input field for user query
- [ ] Add button to trigger RAG query
- [ ] Display RAG response
- [ ] Integrate RAG pipeline components

## 7. Testing & Refinement
- [ ] Add basic unit/integration tests
- [ ] Refine chunking strategy based on results
- [ ] Refine RAG pipeline settings
- [ ] Document usage in README

## 8. Documentation
- [/] Create/Update README.md with setup and usage instructions - *Basic file exists.*
- [ ] Add docstrings to all modules and functions 