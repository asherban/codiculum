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

# Test parsing a valid sample XML file using the memberdef-focused parser
def test_parse_valid_xml_memberdefs(test_data_dir):
    xml_file = test_data_dir / 'sample_doxygen.xml'
    assert xml_file.exists(), f"Test XML file not found at {xml_file}"

    elements = parse_doxygen_xml(xml_file)

    # Expecting 3 elements from memberdefs: function, class, method
    assert len(elements) == 3

    # Check the function element (standalone memberdef)
    func_element = next((el for el in elements if el.id == 'sample_8h_1a1'), None)
    assert func_element is not None
    assert func_element.name == 'sample_function'
    assert func_element.kind == 'function'
    assert func_element.brief_description == 'A sample function.'
    assert func_element.location == CodeLocation(file='sample.h', start_line=10, end_line=8)
    assert 'Type: void' in func_element.detailed_description
    assert 'A sample function.' in func_element.detailed_description
    assert 'More details about the function.' in func_element.detailed_description
    assert 'Signature:' not in func_element.detailed_description

    # Check the class element (memberdef kind='class')
    class_element = next((el for el in elements if el.id == 'classSampleClass'), None)
    assert class_element is not None
    assert class_element.name == 'SampleClass' # Should use compoundname
    assert class_element.kind == 'class'
    assert class_element.brief_description == 'A sample class.'
    # Detailed description for class only includes brief and detailed para
    assert class_element.detailed_description == 'A sample class.\n\nDetailed description of the class.'
    assert class_element.location == CodeLocation(file='sample.h', start_line=15, end_line=25)
    assert 'Signature:' not in class_element.detailed_description

    # Check the method element
    method_element = next((el for el in elements if el.id == 'classSampleClass_1a2'), None)
    assert method_element is not None
    assert method_element.name == 'sample_method'
    assert method_element.kind == 'function'
    assert method_element.brief_description == 'A sample method inside the class.'
    assert method_element.location == CodeLocation(file='sample.h', start_line=20, end_line=23)
    assert 'Type: int' in method_element.detailed_description
    # Method also lacks definition/argsstring in sample XML
    assert 'A sample method inside the class.' in method_element.detailed_description
    # Check exact description based on parser logic (Type + Brief + Detailed Para)
    expected_method_desc = "Type: int\n\nA sample method inside the class.\n\n" # Note trailing newline
    assert method_element.detailed_description == expected_method_desc.strip() # Parser strips final result
    # Check that Signature line is NOT present
    assert 'Signature:' not in method_element.detailed_description

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

