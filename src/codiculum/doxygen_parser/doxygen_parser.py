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
        return " ".join(text.strip() for text in child.itertext() if text.strip())
    # Sometimes text is nested within paragraphs <para>
    para = element.find(f"{tag}/para")
    if para is not None and para.text:
        return para.text.strip()
    # Handle potential mixed content or deeper structures if necessary
    # For now, return None if not found directly or in <para>
    return None


def _get_detailed_description_text(element) -> Optional[str]:
    """Extracts combined text from detaileddescription, handling nested tags."""
    detailed_desc_element = element.find("detaileddescription")
    if detailed_desc_element is None:
        return None
    # Use itertext to get all text content, including nested tags like para, parameterlist, etc.
    # Join the text fragments, stripping whitespace and joining with spaces.
    text_content = " ".join(
        text.strip() for text in detailed_desc_element.itertext() if text.strip()
    )
    return text_content if text_content else None


def _parse_template_params(element: etree.Element) -> Optional[str]:
    """Parses the <templateparamlist> and reconstructs the template<...> string."""
    template_param_list = element.find("templateparamlist")
    if template_param_list is None or len(template_param_list) == 0:
        return None

    params = []
    for param in template_param_list.findall("param"):
        # Get the full type description which might include the name
        param_type_text = _get_text(param, "type")
        ()
        if not param_type_text:
            continue # Skip parameters without type

        # Doxygen might put the whole declaration in <type>, e.g., "typename DerivedTy"
        # Or it might split it into <type>typename</type> and <declname>DerivedTy</declname>
        # We prioritize the full text from <type> if it seems complete.
        param_declname = _get_text(param, "declname")

        param_str = param_type_text
        # If declname exists and is NOT already included at the end of type_text, append it.
        if param_declname and not param_type_text.rstrip().endswith(param_declname):
             param_str = f"{param_type_text} {param_declname}"

        # Fallback for defname - less common but possible
        # param_defname = _get_text(param, "defname")
        # if param_defname and not param_str.rstrip().endswith(param_defname):
        #     param_str = f"{param_str} {param_defname}"
        params.append(param_str.strip())

    if not params:
        return None

    return f"template <{', '.join(params)}>"


def _parse_class_def(compound_def: etree.Element) -> Optional[CodeElement]:
    element_id = compound_def.get("id")
    kind = compound_def.get("kind")
    assert kind == "class"
    name = _get_text(compound_def, "compoundname")
    language = compound_def.get("language")

    if not element_id or not kind or not name:
        logger.warning(
            "Skipping class definition due to missing id, kind, or name"
        )
        return None

    brief_desc = _get_text(compound_def, "briefdescription")
    detailed_desc = _get_detailed_description_text(compound_def)
    template_params = _parse_template_params(compound_def)

    location_element = compound_def.find("location")
    location = None
    if location_element is not None:
        file_path = location_element.get("file")
        bodystart = int(location_element.get("bodystart"))
        bodyend = int(location_element.get("bodyend"))
        try:
            location = CodeLocation(
                file=file_path,
                start_line=bodystart,
                end_line=bodyend,
            )
        except ValueError:
            logger.warning(
                f"Could not parse line numbers for function {name} in {file_path}: bodystart='{bodystart}', bodyend='{bodyend}'"
            )
            return None

    element = CodeElement(
        id=element_id,
        language=language,
        name=name,
        kind=kind,
        brief_description=brief_desc,
        detailed_description=detailed_desc,
        location=location,
        template_params=template_params,
    )
    logger.debug(f"Extracted class element: {name} ({kind}), Template: {template_params}")
    return element

def parse_doxygen_xml_file(xml_file_path: str) -> List[CodeElement]:
    """
    Parses a Doxygen XML file and extracts information about code elements,
    including functions and classes.

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

        # Find all interesting defintisions
        for compound_def in root.findall(".//compounddef"):
            kind = compound_def.get("kind")
            if kind == "class": # TODO: Add other kinds
                element = _parse_class_def(compound_def)
                if element:
                    elements.append(element)

    except etree.XMLSyntaxError as e:
        logger.error(f"Error parsing XML file {xml_file_path}: {e}")
    except FileNotFoundError:
        logger.error(f"XML file not found: {xml_file_path}")
    except Exception as e:
        logger.error(f"An unexpected error occurred while parsing {xml_file_path}: {e}")

    logger.info(
        f"Finished parsing {xml_file_path}. Found {len(elements)} elements (functions/classes)."
    )
    return elements


# Example Usage (requires a sample Doxygen XML file)
if __name__ == "__main__":
    import sys
    import os

    # Setup basic logging for the example
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Assumes the script is run from the project root
    # And the sample LLVM XML data is in 'data/llvm-project/output/xml/'
    # Example: python src/codiculum/doxygen_parser/doxygen_parser.py data/llvm-project/output/xml/index.xml
    # Example: python src/codiculum/doxygen_parser/doxygen_parser.py data/llvm-project/output/xml/namespacellvm.xml
    # Example: python src/codiculum/doxygen_parser/doxygen_parser.py data/llvm-project/output/xml/classllvm_1_1Function.xml

    if len(sys.argv) < 2:
        print("Usage: python doxygen_parser.py <path_to_doxygen_xml_file>")
        # Default to a known file for demonstration if available and no arg provided
        # Adjust this path based on where your sample data actually is
        default_xml_path = os.path.join(
            "data", "llvm-project", "output", "xml", "classllvm_1_1Function.xml"
        )
        if os.path.exists(default_xml_path):
            xml_path = default_xml_path
            print(f"No path provided, attempting default: {xml_path}")
        else:
            print(
                f"Default path {default_xml_path} not found. Please provide an XML file path."
            )
            sys.exit(1)

    else:
        xml_path = sys.argv[1]

    if not os.path.exists(xml_path):
        print(f"Error: XML file not found at {xml_path}")
        sys.exit(1)

    extracted_elements = parse_doxygen_xml_file(xml_path)

    if extracted_elements:
        print(
            f"\nSuccessfully extracted {len(extracted_elements)} elements (functions/classes) from {xml_path}:"
        )
        # Print details of the first few elements as an example
        for i, element in enumerate(extracted_elements[:5]):
            print(f"--- Element {i + 1} ---")
            print(f"  ID: {element.id}")
            print(f"  Name: {element.name}")
            print(f"  Kind: {element.kind}")
            print(f"  Brief: {element.brief_description}")
            # print(f"  Detailed: {element.detailed_description[:100]}...") # Keep output short
            print(
                f"  Detailed Desc (len): {len(element.detailed_description) if element.detailed_description else 0}"
            )
            if element.location:
                print(
                    f"  Location: {element.location.file} (Line: {element.location.start_line}-{element.location.end_line})"
                )
            else:
                print("  Location: Not Available")
    else:
        print(f"No elements (functions/classes) extracted from {xml_path}.")
