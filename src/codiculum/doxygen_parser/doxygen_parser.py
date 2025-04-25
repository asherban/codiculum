# src/codiculum/doxygen_parser/doxygen_parser.py
import logging
from lxml import etree
from typing import List, Optional

from .models import CodeElement, CodeLocation

logger = logging.getLogger(__name__)

def _get_text(element, tag: str) -> Optional[str]:
    """Safely gets the text content of a direct child tag."""
    child = element.find(tag)
    if child is not None and child.text:
        return child.text.strip()
    # Sometimes text is nested within paragraphs <para>
    para = element.find(f'{tag}/para')
    if para is not None and para.text:
        return para.text.strip()
    # Handle potential mixed content or deeper structures if necessary
    # For now, return None if not found directly or in <para>
    return None

def _get_detailed_description_text(element) -> Optional[str]:
    """Extracts combined text from detaileddescription, handling nested tags."""
    detailed_desc_element = element.find('detaileddescription')
    if detailed_desc_element is None:
        return None
    # Use itertext to get all text content, including nested tags like para, parameterlist, etc.
    # Join the text fragments, stripping whitespace and joining with spaces.
    text_content = ' '.join(text.strip() for text in detailed_desc_element.itertext() if text.strip())
    return text_content if text_content else None


def parse_doxygen_xml_file(xml_file_path: str) -> List[CodeElement]:
    """
    Parses a Doxygen XML file and extracts information about code elements,
    specifically focusing on function definitions initially.

    Args:
        xml_file_path: Path to the Doxygen XML file.

    Returns:
        A list of CodeElement objects representing the extracted information.
    """
    logger.info(f"Parsing Doxygen XML file: {xml_file_path}")
    elements: List[CodeElement] = []
    try:
        tree = etree.parse(xml_file_path)
        root = tree.getroot()

        # Doxygen XML structure can vary, look for compounddef and memberdef
        # This example focuses on memberdef within compounddef (like classes/files)
        # We might need to adjust based on the specific XMLs (e.g., index.xml vs specific file xmls)

        # Find all function definitions (can be expanded for classes, variables etc.)
        # Searching globally in the file for memberdef kind=function
        for memberdef in root.xpath('.//memberdef[@kind="function"]'):
            element_id = memberdef.get('id')
            kind = memberdef.get('kind')
            name = _get_text(memberdef, 'name')

            if not element_id or not kind or not name:
                logger.warning(f"Skipping memberdef due to missing id, kind, or name in {xml_file_path}")
                continue

            brief_desc = _get_text(memberdef, 'briefdescription')
            # detailed_desc = _get_text(memberdef, 'detaileddescription') # Simple text grab
            detailed_desc = _get_detailed_description_text(memberdef) # More robust text grab

            location_element = memberdef.find('location')
            location = None
            if location_element is not None:
                file_path = location_element.get('file')
                line = location_element.get('line')
                bodyend = location_element.get('bodyend')
                try:
                    location = CodeLocation(
                        file=file_path,
                        start_line=int(line) if line and line.isdigit() else None,
                        end_line=int(bodyend) if bodyend and bodyend.isdigit() else None
                    )
                except ValueError:
                     logger.warning(f"Could not parse line numbers for {name} in {file_path}: line='{line}', bodyend='{bodyend}'")


            # TODO: Extract signature/parameters more reliably if needed
            # For now, detailed_description often contains it, or use 'argsstring'
            # signature = _get_text(memberdef, 'argsstring') # Removed unused variable assignment


            element = CodeElement(
                id=element_id,
                name=name,
                kind=kind,
                brief_description=brief_desc,
                # Combine signature and detailed description for now? Or store signature separately?
                # Storing detailed description as-is for now.
                detailed_description=detailed_desc,
                location=location,
                # Add signature attribute to CodeElement model if desired
                # signature=signature
            )
            elements.append(element)
            logger.debug(f"Extracted element: {name} ({kind})")

    except etree.XMLSyntaxError as e:
        logger.error(f"Error parsing XML file {xml_file_path}: {e}")
    except FileNotFoundError:
        logger.error(f"XML file not found: {xml_file_path}")
    except Exception as e:
        logger.error(f"An unexpected error occurred while parsing {xml_file_path}: {e}")

    logger.info(f"Finished parsing {xml_file_path}. Found {len(elements)} function elements.")
    return elements

# Example Usage (requires a sample Doxygen XML file)
if __name__ == '__main__':
    import sys
    import os

    # Setup basic logging for the example
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Assumes the script is run from the project root
    # And the sample LLVM XML data is in 'data/llvm-project/output/xml/'
    # Example: python src/codiculum/doxygen_parser/doxygen_parser.py data/llvm-project/output/xml/index.xml
    # Example: python src/codiculum/doxygen_parser/doxygen_parser.py data/llvm-project/output/xml/namespacellvm.xml
    # Example: python src/codiculum/doxygen_parser/doxygen_parser.py data/llvm-project/output/xml/classllvm_1_1Function.xml


    if len(sys.argv) < 2:
        print("Usage: python doxygen_parser.py <path_to_doxygen_xml_file>")
        # Default to a known file for demonstration if available and no arg provided
        # Adjust this path based on where your sample data actually is
        default_xml_path = os.path.join("data", "llvm-project", "output", "xml", "classllvm_1_1Function.xml")
        if os.path.exists(default_xml_path):
             xml_path = default_xml_path
             print(f"No path provided, attempting default: {xml_path}")
        else:
             print(f"Default path {default_xml_path} not found. Please provide an XML file path.")
             sys.exit(1)

    else:
        xml_path = sys.argv[1]

    if not os.path.exists(xml_path):
        print(f"Error: XML file not found at {xml_path}")
        sys.exit(1)

    extracted_elements = parse_doxygen_xml_file(xml_path)

    if extracted_elements:
        print(f"\nSuccessfully extracted {len(extracted_elements)} function elements from {xml_path}:")
        # Print details of the first few elements as an example
        for i, element in enumerate(extracted_elements[:5]):
            print(f"--- Element {i+1} ---")
            print(f"  ID: {element.id}")
            print(f"  Name: {element.name}")
            print(f"  Kind: {element.kind}")
            print(f"  Brief: {element.brief_description}")
            # print(f"  Detailed: {element.detailed_description[:100]}...") # Keep output short
            print(f"  Detailed Desc (len): {len(element.detailed_description) if element.detailed_description else 0}")
            if element.location:
                print(f"  Location: {element.location.file} (Line: {element.location.start_line}-{element.location.end_line})")
            else:
                print("  Location: Not Available")
    else:
        print(f"No function elements extracted from {xml_path}.") 