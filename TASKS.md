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
- [x] Extract relevant information (signatures, docstrings, locations)
- [x] Add error handling for parsing - *Basic handling exists in parser.py*

## 2. Code Chunker (Refer to `docs/ChunkingStrategy.md` for implementation guidelines)
- [x] Step 1: Create chunker module structure (`src/codiculum/chunker/`, `__init__.py`, `code_chunker.py`, `models.py`).
- [x] Step 2: Define `Chunk` data structure in `src/codiculum/chunker/models.py` based on `ChunkingStrategy.md`.
- [ ] Step 3: Define main chunking function signature in `src/codiculum/chunker/code_chunker.py`.
- [ ] Step 4: Implement logic to retrieve source code snippets based on Doxygen location data.
- [ ] Step 5: Implement logic to format a single code element (e.g., function) into a chunk string according to `ChunkingStrategy.md`.
- [ ] Step 6: Implement main loop iterating through parsed Doxygen elements and calling the formatting function.
- [ ] Step 7: Implement logic to handle chunks exceeding token limits (splitting).

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