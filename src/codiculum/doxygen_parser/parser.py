# src/codiculum/doxygen_parser/parser.py
import os
from typing import List, Optional
from lxml import etree
from .models import CodeElement, CodeLocation
from pathlib import Path

def extract_text(element, xpath_query: str) -> Optional[str]:
    """Helper to extract text content cleanly from an element."""
    # Use .// to search within the element's descendants
    node = element.find(xpath_query)
    if node is not None:
        # Concatenate text from all child nodes and tail text
        return "".join(node.itertext()).strip()
    return None

def parse_doxygen_xml(xml_path: Path) -> List[CodeElement]:
    """
    Parses a Doxygen XML file to extract code element information.

    Args:
        xml_path: Path to the Doxygen XML file.

    Returns:
        A list of CodeElement objects extracted from the XML.
    """
    elements: List[CodeElement] = []
    try:
        tree = etree.parse(str(xml_path))
        root = tree.getroot()

        # Process compound definitions (classes, structs, files, namespaces)
        for compounddef in root.xpath('//compounddef'):
            compound_id = compounddef.get('id')
            kind = compounddef.get('kind')
            compound_name = extract_text(compounddef, 'compoundname')
            brief_desc = extract_text(compounddef, 'briefdescription/para')
            detailed_desc = extract_text(compounddef, 'detaileddescription/para')
            location_node = compounddef.find('location')
            location = None
            if location_node is not None:
                location = CodeLocation(
                    file=location_node.get('file'),
                    start_line=int(location_node.get('line', 0)) or None, # Doxygen might omit or use 0
                    end_line=int(location_node.get('bodyend', 0)) or None
                )

            if compound_id and compound_name:
                 elements.append(CodeElement(
                     id=compound_id,
                     name=compound_name,
                     kind=kind or "unknown",
                     brief_description=brief_desc,
                     detailed_description=detailed_desc,
                     location=location
                 ))

            # Process member definitions within sections (functions, variables, enums, etc.)
            for memberdef in compounddef.xpath('.//memberdef[not(@prot="private")]'): # Exclude private members for now
                member_id = memberdef.get('id')
                member_kind = memberdef.get('kind')
                member_name = extract_text(memberdef, 'name')
                member_type = extract_text(memberdef, 'type')
                definition = extract_text(memberdef, 'definition')
                argsstring = extract_text(memberdef, 'argsstring')
                brief_desc = extract_text(memberdef, 'briefdescription/para')
                detailed_desc = extract_text(memberdef, 'detaileddescription/para') # Might need more complex extraction for params

                member_location_node = memberdef.find('location')
                member_location = None
                if member_location_node is not None:
                    member_location = CodeLocation(
                        file=member_location_node.get('file'),
                        start_line=int(member_location_node.get('line', 0)) or None,
                        end_line=int(member_location_node.get('bodyend', 0)) or None
                    )

                # Construct a more complete description/signature
                full_desc = f'''Type: {member_type}
Definition: {definition}{argsstring}

{detailed_desc or ''}'''

                if member_id and member_name:
                    elements.append(CodeElement(
                        id=member_id,
                        name=member_name,
                        kind=member_kind or "unknown",
                        brief_description=brief_desc,
                        detailed_description=full_desc.strip(), # Use the constructed description
                        location=member_location
                    ))

    except etree.XMLSyntaxError as e:
        print(f"Error parsing XML file {xml_path}: {e}")
    except FileNotFoundError:
        print(f"Error: XML file not found at {xml_path}")
    except Exception as e:
        print(f"An unexpected error occurred while parsing {xml_path}: {e}")

    return elements

# Example usage for demonstration
if __name__ == '__main__':
    # Use a specific, potentially interesting XML file from the Doxygen output
    # Ensure this path is correct relative to the project root
    test_xml_path = Path('data/llvm-project/output/xml/classllvm_1_1SmallVector.xml')

    print(f"Attempting to parse: {test_xml_path.resolve()}")

    if test_xml_path.exists():
        extracted_elements = parse_doxygen_xml(test_xml_path)
        print("\n" + f"--- Extracted {len(extracted_elements)} elements from {test_xml_path.name} ---")
        if not extracted_elements:
             print("No elements extracted. Check the XML structure and XPath queries.")
        for i, element in enumerate(extracted_elements):
            print("\n" + f"Element {i+1}:")
            print(f"  ID: {element.id}")
            print(f"  Name: {element.name}")
            print(f"  Kind: {element.kind}")
            print(f"  Brief: {element.brief_description}")
            # print(f"  Detailed: {element.detailed_description}") # Often long, uncomment if needed
            if element.location:
                print(f"  Location: {element.location.file} (Lines: {element.location.start_line}-{element.location.end_line})")
            else:
                print("  Location: Not specified")
    else:
        print(f"Error: Test XML file not found at {test_xml_path}")
        print("Please ensure Doxygen has been run and the XML file exists at the specified path.")
        print("Current working directory:", Path.cwd()) 