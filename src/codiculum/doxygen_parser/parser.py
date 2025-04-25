# src/codiculum/doxygen_parser/parser.py
import os
from typing import List, Optional
from lxml import etree
from codiculum.doxygen_parser.models import CodeElement, CodeLocation
from pathlib import Path

def extract_text(element, xpath_query: str) -> Optional[str]:
    """Helper to extract text content cleanly from an element."""
    node = element.find(xpath_query)
    if node is not None:
        # Concatenate text from all child nodes and tail text, handle potential None
        text_content = "".join(t for t in node.itertext() if t).strip()
        return text_content if text_content else None # Return None if empty after stripping
    return None

def parse_doxygen_xml(xml_path: Path) -> List[CodeElement]:
    """
    Parses a Doxygen XML file to extract code element information directly from member definitions.
    Focuses on memberdef elements (functions, classes, methods, variables, etc.).

    Args:
        xml_path: Path to the Doxygen XML file.

    Returns:
        A list of CodeElement objects extracted from the memberdef elements in the XML.
    """
    elements: List[CodeElement] = []
    try:
        tree = etree.parse(str(xml_path))
        root = tree.getroot()

        # Find all member definitions globally, excluding private ones
        for memberdef in root.xpath('//memberdef[not(@prot="private")]'):
            member_id = memberdef.get('id')
            member_kind = memberdef.get('kind')

            # Determine name based on kind
            member_name = None
            if member_kind in ['class', 'struct', 'interface', 'namespace']:
                member_name = extract_text(memberdef, 'compoundname')
            else:
                member_name = extract_text(memberdef, 'name')

            # Skip if essential info is missing
            if not member_id or not member_name:
                # print(f"Skipping memberdef due to missing ID ('{member_id}') or Name ('{member_name}'). Kind: {member_kind}")
                continue

            member_type = extract_text(memberdef, 'type')
            definition = extract_text(memberdef, 'definition')
            argsstring = extract_text(memberdef, 'argsstring')
            brief_desc = extract_text(memberdef, 'briefdescription/para')
            detailed_desc_para = extract_text(memberdef, 'detaileddescription/para')

            # Location extraction
            member_location_node = memberdef.find('location')
            member_location = None
            if member_location_node is not None:
                file_attr = member_location_node.get('file')
                start_line_attr = member_location_node.get('line')
                end_line_attr = member_location_node.get('bodyend')
                if file_attr:
                    member_location = CodeLocation(
                        file=file_attr,
                        start_line=int(start_line_attr) if start_line_attr and start_line_attr != '0' else None,
                        end_line=int(end_line_attr) if end_line_attr and end_line_attr != '0' else None
                    )

            # Construct signature/description based on kind
            full_desc = brief_desc or ""
            signature = None
            if member_kind in ['function', 'variable', 'enum', 'typedef']: # Kinds that typically have type/definition/args
                 # Combine definition and argsstring if both exist, handle potential None values
                signature_parts = [part for part in [definition, argsstring] if part]
                signature = " ".join(signature_parts)
                type_info = f"Type: {member_type or 'N/A'}\n" if member_type else ""
                sig_info = f"Signature: {signature or 'N/A'}\n" if signature else ""
                full_desc = f"{type_info}{sig_info}\n{brief_desc or ''}\n\n{detailed_desc_para or ''}"
            else: # For classes/structs, just use brief/detailed
                full_desc = f"{brief_desc or ''}\n\n{detailed_desc_para or ''}"


            elements.append(CodeElement(
                id=member_id,
                name=member_name,
                kind=member_kind or "unknown",
                brief_description=brief_desc, # Keep brief separate for potential use
                detailed_description=full_desc.strip(),
                location=member_location
            ))

    except etree.XMLSyntaxError as e:
        print(f"Error parsing XML file {xml_path}: {e}")
    except IOError as e: # Catch IOError for file not found before generic Exception
        print(f"Error: XML file not found or cannot be read at {xml_path}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while parsing {xml_path} ({type(e).__name__}): {e}")

    return elements

# Example usage for demonstration
if __name__ == '__main__':
    # Use a specific, potentially interesting XML file from the Doxygen output
    # Ensure this path is correct relative to the project root
    # test_xml_path = Path('data/llvm-project/output/xml/classllvm_1_1SmallVector.xml') # Example class
    test_xml_path = Path('tests/doxygen_parser/test_data/sample_doxygen.xml') # Use sample for demo

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
            print(f"  Detailed: {element.detailed_description}")
            if element.location:
                print(f"  Location: {element.location.file} (Lines: {element.location.start_line}-{element.location.end_line})")
            else:
                print("  Location: Not specified")
    else:
        print(f"Error: Test XML file not found at {test_xml_path}")
        print("Please ensure Doxygen has been run and the XML file exists at the specified path.")
        print("Current working directory:", Path.cwd()) 