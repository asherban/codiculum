import pytest
from pathlib import Path
# import lxml.etree as ET # Removed unused import

# from codiculum.doxygen_parser.parser import parse_doxygen_xml, extract_text # Removed unused extract_text
from codiculum.doxygen_parser.parser import parse_doxygen_xml
# from codiculum.doxygen_parser.models import CodeElement, CodeLocation # Removed unused CodeElement
from codiculum.doxygen_parser.models import CodeLocation

# Fixture to provide the path to the test XML data directory
@pytest.fixture
def test_data_dir(tmp_path):
    # Create a dummy test data directory for structure, real data is checked-in
    data_dir = Path(__file__).parent / 'test_data'
    return data_dir

# Test parsing a non-existent file
def test_parse_non_existent_file(tmp_path, capsys):
    non_existent_file = tmp_path / 'non_existent.xml'
    elements = parse_doxygen_xml(non_existent_file)
    assert elements == []
    captured = capsys.readouterr()
    # Updated Assertion: Match the IOError message format
    assert f"Error: XML file not found or cannot be read at {non_existent_file}" in captured.out

# Test parsing an invalid XML file
def test_parse_invalid_xml(tmp_path, capsys):
    invalid_xml_file = tmp_path / 'invalid.xml'
    invalid_xml_file.write_text("<root><unclosed></root>") # Malformed XML
    elements = parse_doxygen_xml(invalid_xml_file)
    assert elements == []
    captured = capsys.readouterr()
    assert f"Error parsing XML file {invalid_xml_file}" in captured.out

