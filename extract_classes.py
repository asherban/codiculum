import xml.etree.ElementTree as ET
import os
import argparse
import sys

def extract_class_code_from_xml(xml_dir, source_root):
    """
    Parses Doxygen XML files to find class definitions and extracts their code.

    Args:
        xml_dir: The directory containing the Doxygen XML output files.
        source_root: The root directory of the source code referenced in the XML.
    """
    print(f"Scanning XML files in: {xml_dir}")
    print(f"Using source root: {source_root}\n")

    found_classes = False
    kinds_to_extract = {'class', 'struct', 'interface', 'enum', 'example'} # Add others if needed

    max_tokens = 0
    num_classes = 0

    for root, _, files in os.walk(xml_dir):
        for filename in files:
            if not filename.endswith('.xml') or filename == 'index.xml':
                continue

            xml_filepath = os.path.join(root, filename)

            try:
                tree = ET.parse(xml_filepath)
                xml_root = tree.getroot()

                # Find all compound definitions in this file
                for compound_def in xml_root.findall('.//compounddef'):
                    kind = compound_def.get('kind')
                    if kind in kinds_to_extract:
                        compound_name_element = compound_def.find('compoundname')
                        if compound_name_element is None or not compound_name_element.text:
                            print(f"Warning: Skipping compound of kind '{kind}' in {filename} - missing name.", file=sys.stderr)
                            continue
                        class_name = compound_name_element.text

                        location = compound_def.find('location')
                        if location is None:
                            print(f"Warning: Skipping class '{class_name}' in {filename} - missing <location>.", file=sys.stderr)
                            continue

                        source_rel_path = location.get('file')
                        start_line_str = location.get('line')
                        end_line_str = location.get('bodyend') # Use bodyend for the end of the definition block

                        if not source_rel_path or not start_line_str or not end_line_str:
                            print(f"Warning: Skipping class '{class_name}' in {filename} - missing location attributes (file/line/bodyend).", file=sys.stderr)
                            continue

                        try:
                            start_line = int(start_line_str)
                            end_line = int(end_line_str)
                        except ValueError:
                            print(f"Warning: Skipping class '{class_name}' in {filename} - invalid line numbers ('{start_line_str}', '{end_line_str}').", file=sys.stderr)
                            continue

                        # Construct full path to the source file
                        source_abs_path = os.path.abspath(os.path.join(source_root, source_rel_path))

                        print(f"--- Found Class: {class_name} ---")
                        print(f"  Source File: {source_abs_path}")
                        print(f"  Lines: {start_line}-{end_line}")

                        found_classes = True

                        # Extract code snippet
                        try:
                            num_classes += 1
                            with open(source_abs_path, 'r', encoding='utf-8', errors='ignore') as f:
                                lines = f.readlines()
                                # XML line numbers are 1-based, Python list index is 0-based
                                code_snippet = "".join(lines[start_line-1:end_line])
                                print("  Code:")
                                print("-" * 60)
                                print(code_snippet.strip())
                                print("-" * 60)
                                print("\n")
                                snippet_len = len(code_snippet.strip())
                                if snippet_len > max_tokens:
                                    max_tokens = snippet_len

                        except FileNotFoundError:
                            print(f"  Error: Source file not found at {source_abs_path}\n", file=sys.stderr)
                        except IndexError:
                             print(f"  Error: Line numbers ({start_line}-{end_line}) out of bounds for file {source_abs_path} (total lines: {len(lines)})\n", file=sys.stderr)
                        except Exception as e:
                            print(f"  Error reading source file {source_abs_path}: {e}\n", file=sys.stderr)

            except ET.ParseError as e:
                print(f"Error parsing XML file {xml_filepath}: {e}", file=sys.stderr)
            except Exception as e:
                 print(f"An unexpected error occurred processing {xml_filepath}: {e}", file=sys.stderr)

    print(f"Total classes found: {num_classes}")
    print(f"Maximum tokens in any class: {max_tokens}")
    if not found_classes:
        print("No class definitions found in the XML files.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract class source code using Doxygen XML output.")
    parser.add_argument("xml_dir", help="Directory containing the Doxygen XML files.")
    parser.add_argument("source_root", help="Root directory of the source code referenced in the XML.")

    args = parser.parse_args()

    if not os.path.isdir(args.xml_dir):
        print(f"Error: XML directory not found: {args.xml_dir}", file=sys.stderr)
        sys.exit(1)

    if not os.path.isdir(args.source_root):
        print(f"Error: Source root directory not found: {args.source_root}", file=sys.stderr)
        sys.exit(1)

    extract_class_code_from_xml(args.xml_dir, args.source_root)
