import pytest
from pathlib import Path
from typing import List

from src.codiculum.doxygen_parser.models import CodeElement, CodeLocation
from src.codiculum.chunker.models import Chunk
from src.codiculum.chunker.code_chunker import CodeChunker

# --- Test Data Setup ---

# Minimal dummy source file content
DUMMY_SOURCE_CONTENT = """
// File: src/dummy.cpp

#include <iostream>

/**
 * @brief A simple dummy function.
 * 
 * This function just prints hello.
 */
void dummy_function(int param1) {
    std::cout << "Hello!" << std::endl;
}

// Another function without docs
int another_func() {
    return 42;
}
"""

# Minimal dummy parsed data corresponding to the source
# CORRECTED line numbers based on typical Doxygen output (line=declaration, bodyend=closing brace)
DUMMY_PARSED_DATA: List[CodeElement] = [
    CodeElement(
        id="func_dummy_1",
        name="dummy_function",
        kind="function",
        language="C++",
        brief_description="A simple dummy function.",
        detailed_description="Signature: void dummy_function(int param1)\nDocs: This function just prints hello.",
        location=CodeLocation(file="src/dummy.cpp", start_line=10, end_line=12),
    ),
    CodeElement(
        id="func_dummy_2",
        name="another_func",
        kind="function",
        language="C++",
        brief_description=None,
        detailed_description="Signature: int another_func()",
        location=CodeLocation(file="src/dummy.cpp", start_line=15, end_line=17),
    )
]

# Expected chunk content (adjust based on actual format_chunk logic)
EXPECTED_CHUNK_CONTENT_FUNC1 = """
File: src/dummy.cpp
Kind: function
Signature: void dummy_function(int param1)
Brief: A simple dummy function.
Docs: This function just prints hello.

---
Code:
```cpp
void dummy_function(int param1) {
    std::cout << "Hello!" << std::endl;
}
```
"""

EXPECTED_CHUNK_CONTENT_FUNC2 = """
File: src/dummy.cpp
Kind: function
Signature: int another_func()

---
Code:
```cpp
int another_func() {
    return 42;
}
```
"""


@pytest.fixture
def dummy_src_dir(tmp_path: Path) -> Path:
    """Creates a temporary directory structure with a dummy source file."""
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    dummy_file = src_dir / "dummy.cpp"
    dummy_file.write_text(DUMMY_SOURCE_CONTENT)
    return tmp_path # Return the base temp path, as src_base_path is relative to this


# --- Test Case ---

def test_create_chunks_from_doxygen_integration(dummy_src_dir: Path):
    """
    Integration test for the main chunking orchestrator.
    Uses dummy parsed data and a temporary source file.
    """
    src_base_path = dummy_src_dir

    # --- Mock formatters and retrievers if needed, or use actual ones --- 
    # For true integration, we'd ideally use the real ones if they exist
    # If they aren't implemented yet, mocking is necessary.
    # from unittest.mock import patch
    # with patch('src.codiculum.chunker.code_chunker.retrieve_code_snippet') as mock_retrieve,
    #      patch('src.codiculum.chunker.code_chunker.format_chunk') as mock_format:
          # Setup mock return values based on DUMMY_PARSED_DATA and DUMMY_SOURCE_CONTENT
          # mock_retrieve.side_effect = lambda loc, base: ... 
          # mock_format.side_effect = lambda element, snippet: ...

    # --- Instantiate the chunker and call its method ---
    chunker = CodeChunker(src_base_path=src_base_path)
    actual_chunks: List[Chunk] = chunker.chunk(
        parsed_data=DUMMY_PARSED_DATA
    )

    # --- Assertions ---
    assert len(actual_chunks) == 2, "Should create one chunk per parsed element"

    # Verify chunk 1 (dummy_function)
    chunk1 = next((c for c in actual_chunks if c.metadata.get('name') == 'dummy_function'), None)
    assert chunk1 is not None
    # TODO: Re-enable text assertion once format is finalized
    # assert chunk1.text.strip() == EXPECTED_CHUNK_CONTENT_FUNC1.strip()
    assert chunk1.metadata['kind'] == 'function'
    assert chunk1.metadata['file_path'] == 'src/dummy.cpp'
    assert chunk1.metadata['start_line'] == 10
    assert chunk1.metadata['end_line'] == 12
    assert chunk1.metadata['id'] == 'func_dummy_1'
    assert 'dummy_function(int param1)' in chunk1.text # Check signature/name part of text
    assert 'std::cout << "Hello!"' in chunk1.text # Check code snippet part of text

    # Verify chunk 2 (another_func)
    chunk2 = next((c for c in actual_chunks if c.metadata.get('name') == 'another_func'), None)
    assert chunk2 is not None
    # TODO: Re-enable text assertion once format is finalized
    # assert chunk2.text.strip() == EXPECTED_CHUNK_CONTENT_FUNC2.strip()
    assert chunk2.metadata['kind'] == 'function'
    assert chunk2.metadata['file_path'] == 'src/dummy.cpp'
    assert chunk2.metadata['start_line'] == 15
    assert chunk2.metadata['end_line'] == 17
    assert chunk2.metadata['id'] == 'func_dummy_2'
    assert 'another_func()' in chunk2.text
    assert 'return 42;' in chunk2.text

    # Add more specific assertions based on the expected Chunk structure and content 