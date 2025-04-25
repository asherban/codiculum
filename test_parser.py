from pathlib import Path
from src.codiculum.doxygen_parser.parser import parse_doxygen_xml

# Replace with the actual path to your Doxygen XML file if different
xml_file_path = Path('data/llvm-project/output/xml/index.xml')

if xml_file_path.exists():
    print(f"--- Parsing {xml_file_path} ---")
    parse_doxygen_xml(xml_file_path)
    print("--- Parsing finished ---")
else:
    print(f"Error: Test XML file not found at {xml_file_path}")
    print("Please ensure Doxygen XML output exists at this location or modify the path.") 