# Project Tasks

## Project Setup
- [x] Initialize project structure (directories, basic files)
- [x] Setup `pyproject.toml` with `uv`
- [x] Review existing Python files (`main.py`, `extract_classes.py`) and integrate or remove.
- [x] Add initial dependencies (`llama-index`, `chromadb`, `openai`, `streamlit`, `lxml`) using `uv add`
- [x] Initial commit
- [x] Configure pytest to run tests only from the `tests` directory.

## 1. Doxygen Parser
- [x] Identify target Doxygen XML files/structure (`data/llvm-project/output/xml/`)
- [x] Define data structure(s) for extracted code elements (`src/codiculum/doxygen_parser/models.py`)
- [x] Implement and test Doxygen XML parsing for functions/classes (`src/codiculum/doxygen_parser/parser.py`). (Visible outcome: Parser function successfully processes sample XML and returns extracted data structures; includes basic error handling; verified via test or demo script).
- [x] The doxygen parser component does not have tests - add unit tests.
- [x] Enhance parser to correctly extract class definitions (`compounddef[@kind='class']`).
- [x] Enhance parser to extract template parameters for C++ classes (model and parser logic).

## 2. Code Chunker (Refer to `docs/ChunkingStrategy.md`)
- [x] Create chunker module structure (`src/codiculum/chunker/`) and define `Chunk` model (`src/codiculum/chunker/models.py`).
- [x] Implement and test source code snippet retrieval based on Doxygen location data. (Visible outcome: Function takes Doxygen location, returns code string; verified via unit test).
- [x] Implement and test formatting of a single code element into a `Chunk` object. (Visible outcome: Function takes parsed element data & source, returns `Chunk` object according to strategy; verified via unit test).
- [x] Implement and test the main chunking orchestrator function (`src/codiculum/chunker/code_chunker.py`). (Visible outcome: Function takes parsed Doxygen data, orchestrates retrieval/formatting, returns list of `Chunk` objects; verified via integration test using sample data).
- [x] Implement a UI to test the doxygen parser and code chunker visually (`app.py`). (Visible outcome: `uv run streamlit run app.py` launches UI allowing XML selection, element selection, and chunk display).
- [x] Update chunk formatting to include C++ template parameters and verify via integration test.
- [x] Fix template parameter parsing and update chunk formatting to include C++ template signature within the code block, verified via tests.

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
- [x] Display source file content alongside chunk in Streamlit app.

## 7. Refinement & End-to-End Testing
- [ ] Perform end-to-end testing using representative Doxygen data and user queries.
- [ ] Refine chunking strategy based on end-to-end test results.
- [ ] Refine RAG pipeline settings (retriever, synthesizer) based on end-to-end test results.

## 8. Documentation
- [ ] Update README.md with comprehensive setup, usage instructions, and architecture overview.
- [ ] Perform final review and add/update docstrings for all public modules and functions.

## Testing
- [x] Fix TypeError in `tests/chunker/test_code_chunker.py::test_format_element_to_chunk`
- [x] Fix AssertionError in `tests/chunker/test_code_chunker_integration.py` (metadata key mismatch)

## Doxygen XML Parser
- [ ] Display source file content alongside chunk in Streamlit app.

## Project Setup & Core Dependencies
- [x] Initialize project structure (`src`, `tests`, `data`)
- [x] Set up `uv` and `pyproject.toml` with basic dependencies (`llama-index`, `chromadb`, `openai`, `streamlit`, `lxml`, `pytest`)
- [x] Configure basic `pytest` setup (`pytest.ini`, simple test in `tests/`)
- [x] Create initial `TASKS.md` file.
- [x] Add `.gitignore`.

## Doxygen Parser (`codiculum.doxygen_parser`)
- [x] Step 1: Add `lxml` dependency via `uv add lxml` and verify installation.
- [x] Step 2: Define data structure for extracted info (e.g., `FunctionInfo`, `ClassInfo`, `FileInfo`, `Location`) in `src/codiculum/doxygen_parser/models.py`.
- [x] Step 3: Implement function: parse single `<compounddef>` (file) element in `src/codiculum/doxygen_parser/_parser.py`. Add test `tests/doxygen_parser/test_parse_compounddef_file.py`.
- [x] Step 4: Implement function: parse single `<compounddef>` (class/struct) element in `src/codiculum/doxygen_parser/_parser.py`. Add test `tests/doxygen_parser/test_parse_compounddef_class.py`.
- [x] Step 5: Implement function: parse single `<memberdef>` (function/method) element in `src/codiculum/doxygen_parser/_parser.py`. Add test `tests/doxygen_parser/test_parse_memberdef_function.py`.
- [x] Step 6: Implement main entry point `parse_doxygen_xml_file(xml_path)` and `parse_doxygen_xml_dir(dir_path)` in `src/codiculum/doxygen_parser/__init__.py`. Add integration test `tests/doxygen_parser/test_parser_integration.py`.
- [x] Step 7: Refine parsing to extract detailed description (`briefdescription`, `detaileddescription`) from elements. Update tests.
- [x] Step 8: Handle `@param` and `@return` documentation within function/method memberdefs. Update `FunctionInfo` model and parser logic. Update tests.

## Code Chunker (`codiculum.chunker`)
- [x] Step 1: Define `CodeChunk` data structure (`text`, `metadata` including `id`, `kind`, `name`, `file_path`, `start_line`, `end_line`, `url`, `signature`, `docstring`).
- [x] Step 2: Implement `CodeChunker` class in `src/codiculum/chunker.py`.
- [x] Step 3: Implement chunking logic for functions/methods within `CodeChunker.chunk()`. Use `Location` info and read source file content. Add test `tests/chunker/test_chunk_function.py`.
- [x] Step 4: Implement chunking logic for classes/structs within `CodeChunker.chunk()`. Include signature/definition and docstring. Add test `tests/chunker/test_chunk_class.py`.
- [x] Step 5: Handle potential file reading errors gracefully during chunking. Add test case for missing file.
- [x] Step 6: Refine metadata stored in `CodeChunk` (e.g., add qualified name).
- [x] Step 7: Add URL generation based on repo structure (e.g., GitHub link structure) if `repo_url` is provided.

## Streamlit UI (`app.py`)
- [x] Step 1: Create basic Streamlit app (`app.py`) to list Doxygen XML files from a specified directory (`data/doxygen_output/xml`).
- [x] Step 2: Add dropdown to select an XML file.
- [x] Step 3: On file selection, call `parse_doxygen_xml_file`.
- [x] Step 4: Display parsed element names (functions, classes) in a selectable list/dropdown.
- [x] Step 5: Instantiate `CodeChunker` and call `.chunk()` on the parsed data.
- [x] Step 6: When an element is selected, display the corresponding generated `CodeChunk` text and metadata.
- [x] Display source file content alongside chunk in Streamlit app.

## Embedding & Vector Store (`codiculum.embedding`, `codiculum.vector_store`)
- [ ] Step 1: Define `EmbeddingGenerator` interface/class using OpenAI API.
- [ ] Step 2: Implement `VectorStoreManager` interface/class using ChromaDB.
- [ ] Step 3: Integrate LlamaIndex `ChromaVectorStore`.
- [ ] Step 4: Create script (`scripts/generate_embeddings.py`) to:
    *   Parse Doxygen XML directory.
    *   Chunk the parsed data.
    *   Generate embeddings for chunks.
    *   Store chunks and embeddings in ChromaDB.

## RAG Pipeline (`codiculum.rag`)
- [ ] Step 1: Implement basic RAG query engine using LlamaIndex, ChromaDB vector store, and OpenAI LLM.
- [ ] Step 2: Integrate RAG engine into the Streamlit app for querying.

## Testing & Refinement
- [ ] Add more comprehensive integration tests.
- [ ] Refine chunking strategy based on initial RAG results.
- [ ] Add error handling and logging throughout the application.
- [ ] Create `README.md` with setup and usage instructions.

## Documentation
- [ ] Add docstrings to all public modules, classes, and functions.
- [ ] Generate project documentation (e.g., using Sphinx or MkDocs).

## Future Enhancements
- [ ] Support for other languages/Doxygen outputs.
- [ ] More sophisticated chunking strategies (e.g., recursive splitting).
- [ ] Integration with different vector stores or embedding models.
- [ ] Evaluation framework for RAG performance.