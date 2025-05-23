# import pytest # Removed unused import
# from pathlib import Path # Removed unused import
from src.codiculum.doxygen_parser.models import CodeElement, CodeLocation
from src.codiculum.chunker.models import Chunk
from src.codiculum.chunker.code_chunker import format_element_to_chunk

def test_format_element_to_chunk():
    """Test formatting a simple CodeElement into a Chunk."""
    element = CodeElement(
        id="test_func_1",
        name="test_function",
        kind="function",
        language="python",
        brief_description="A test function.",
        detailed_description="Does nothing useful.",
        location=CodeLocation(
            file="src/example.py",
            start_line=5,
            end_line=10
        )
    )
    source_snippet = "def test_function():\n    print('Hello')\n"

    # Construct the expected text representation for the chunk
    # Template params (empty in this case) are now prepended to the code snippet
    expected_code_block = f"```python\n{source_snippet}\n```"
    expected_text = f"""File: src/example.py
Brief: {element.brief_description}
Detailed: {element.detailed_description}

Code:
{expected_code_block}"""

    expected_chunk = Chunk(
        text=expected_text,
        metadata={
            "id": "test_func_1",
            "name": "test_function",
            "kind": "function",
            "file_path": "src/example.py",
            "start_line": 5,
            "end_line": 10,
            "brief_description": "A test function.",
            "detailed_description": "Does nothing useful.",
            "template_params": "",
        }
    )

    # TODO: Implement format_element_to_chunk in src/codiculum/chunker/code_chunker.py
    actual_chunk = format_element_to_chunk(element, source_snippet)

    assert actual_chunk == expected_chunk 