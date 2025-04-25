# Project Tasks

## Project Setup
- [x] Initialize project structure (directories, basic files)
- [x] Setup `pyproject.toml` with `uv`
- [x] Review existing Python files (`main.py`, `extract_classes.py`) and integrate or remove.
- [x] Add initial dependencies (`llama-index`, `chromadb`, `openai`, `streamlit`, `lxml`) using `uv add`
- [x] Initial commit

## 1. Doxygen Parser
- [x] Identify target Doxygen XML files/structure (`data/llvm-project/output/xml/`)
- [x] Define data structure(s) for extracted code elements (`src/codiculum/doxygen_parser/models.py`)
- [x] Implement and test Doxygen XML parsing for functions/classes (`src/codiculum/doxygen_parser/parser.py`). (Visible outcome: Parser function successfully processes sample XML and returns extracted data structures; includes basic error handling; verified via test or demo script).

## 2. Code Chunker (Refer to `docs/ChunkingStrategy.md`)
- [x] Create chunker module structure (`src/codiculum/chunker/`) and define `Chunk` model (`src/codiculum/chunker/models.py`).
- [x] Implement and test source code snippet retrieval based on Doxygen location data. (Visible outcome: Function takes Doxygen location, returns code string; verified via unit test).
- [ ] Implement and test formatting of a single code element into a `Chunk` object. (Visible outcome: Function takes parsed element data & source, returns `Chunk` object according to strategy; verified via unit test).
- [ ] Implement and test the main chunking orchestrator function (`src/codiculum/chunker/code_chunker.py`). (Visible outcome: Function takes parsed Doxygen data, orchestrates retrieval/formatting, returns list of `Chunk` objects; verified via integration test using sample data).
- [ ] Implement and test chunk splitting logic for token limits. (Visible outcome: Main chunker function splits large chunks; verified by updating integration test).

## 3. Embedding Generator
- [ ] Implement and test embedding generation function using OpenAI. (Visible outcome: Function takes list of `Chunk` objects, returns embeddings; handles API errors; verified via unit test with mocked API calls).

## 4. Vector Store Manager (ChromaDB)
- [ ] Implement and test ChromaDB initialization and `VectorStore` configuration. (Visible outcome: Script/function successfully initializes a persistent ChromaDB client and LlamaIndex `ChromaVectorStore`; verified by checking DB file creation/loading).
- [ ] Implement and test adding/updating chunk embeddings in ChromaDB. (Visible outcome: Function adds LlamaIndex `Node` objects to the store; verified via test script adding data and checking store count/retrieval).

## 5. RAG Pipeline (LlamaIndex)
- [ ] Implement and test `VectorStoreIndex` creation from ChromaDB. (Visible outcome: Function loads store and builds index; verified by logging index properties or successful creation).
- [ ] Implement and test the core RAG query engine. (Visible outcome: Function `query_codebase(query_text)` loads index, runs query, returns response structure; verified via test script with sample query against pre-loaded data).

## 6. Streamlit UI
- [ ] Create basic Streamlit app layout (`app.py`). (Visible outcome: `uv run streamlit run app.py` shows input field, button, output area).
- [ ] Integrate RAG query functionality into Streamlit app. (Visible outcome: App takes user query, calls RAG engine on button click, displays response).

## 7. Refinement & End-to-End Testing
- [ ] Perform end-to-end testing using representative Doxygen data and user queries.
- [ ] Refine chunking strategy based on end-to-end test results.
- [ ] Refine RAG pipeline settings (retriever, synthesizer) based on end-to-end test results.

## 8. Documentation
- [ ] Update README.md with comprehensive setup, usage instructions, and architecture overview.
- [ ] Perform final review and add/update docstrings for all public modules and functions.