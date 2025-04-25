import pytest
from src.codiculum.doxygen_parser.models import CodeElement, CodeLocation
from src.codiculum.chunker.models import Chunk
from src.codiculum.chunker.code_chunker import format_element_to_chunk

def test_format_element_to_chunk():
    """Test formatting a simple CodeElement into a Chunk."""
    element = CodeElement(
        id="test_func_1",
        name="test_function",
        kind="function",
        brief_description="A test function.",
        detailed_description="Does nothing useful.",
        location=CodeLocation(
            file="src/example.py",
            start_line=5,
            end_line=10
        )
    )
    source_snippet = "def test_function():\n    print('Hello')\n"

    expected_chunk = Chunk(
        filename="src/example.py",
        start_line=5,
        end_line=10,
        code_snippet=source_snippet,
        brief_description="A test function.",
        detailed_description="Does nothing useful.",
        # Other fields like imports, usage_examples, is_partial can be None/default for now
    )

    # This will fail initially as format_element_to_chunk is not implemented
    actual_chunk = format_element_to_chunk(element, source_snippet)

    assert actual_chunk == expected_chunk 