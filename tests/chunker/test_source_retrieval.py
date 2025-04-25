import pytest
from pathlib import Path

# Import the function directly now
from src.codiculum.chunker.source_retriever import retrieve_source_snippet

SAMPLE_CODE_PATH = Path(__file__).parent / "sample_code.cpp"

def test_retrieve_function_snippet():
    """Tests retrieving a specific function body."""
    # Lines 4-10 of sample_code.cpp contain the 'add' function
    expected_snippet = (
        "int add(int a, int b) {\n"
        "    // Check for positive numbers\n"
        "    if (a > 0 && b > 0) {\n"
        "        return a + b; // Add them\n"
        "    }\n"
        "    return 0; // Return 0 otherwise\n"
        "}"
    )
    # No need to import inside anymore
    actual_snippet = retrieve_source_snippet(str(SAMPLE_CODE_PATH), start_line=4, end_line=10)
    assert actual_snippet == expected_snippet

def test_retrieve_class_snippet():
    """Tests retrieving a specific class body."""
    # Lines 13-22 of sample_code.cpp contain the 'MyClass' definition
    expected_snippet = (
        "class MyClass {\n"
        "public:\n"
        "    int value;\n\n"
        "    MyClass(int v) : value(v) {}\n\n"
        "    void printValue() {\n"
        "        std::cout << \"Value: \" << value << std::endl;\n"
        "    }\n"
        "};"
    )
    # No need to import inside anymore
    actual_snippet = retrieve_source_snippet(str(SAMPLE_CODE_PATH), start_line=13, end_line=22)
    assert actual_snippet == expected_snippet

def test_retrieve_single_line():
    """Tests retrieving a single line."""
    # Line 15 is "    int value;"
    expected_snippet = "    int value;"
    # No need to import inside anymore
    actual_snippet = retrieve_source_snippet(str(SAMPLE_CODE_PATH), start_line=15, end_line=15)
    assert actual_snippet == expected_snippet

def test_file_not_found():
    """Tests behavior when the source file does not exist."""
    with pytest.raises(FileNotFoundError):
        # No need to import inside anymore
        retrieve_source_snippet("non_existent_file.cpp", 1, 5)

def test_invalid_line_numbers():
    """Tests behavior with invalid line numbers."""
    with pytest.raises(ValueError):
        # No need to import inside anymore
        retrieve_source_snippet(str(SAMPLE_CODE_PATH), start_line=0, end_line=5) # Start line < 1
    with pytest.raises(ValueError):
        retrieve_source_snippet(str(SAMPLE_CODE_PATH), start_line=5, end_line=3) # end < start
    with pytest.raises(IndexError): # Expecting IndexError now based on implementation
        retrieve_source_snippet(str(SAMPLE_CODE_PATH), start_line=100, end_line=105) # Lines beyond file length 