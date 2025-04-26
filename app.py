import streamlit as st
from pathlib import Path
from codiculum.doxygen_parser import parse_doxygen_xml_file
from codiculum.chunker import CodeChunker

# Define the directory containing Doxygen XML files
SOURCE_BASE_DIR = Path("data/llvm-project")
DOXYGEN_XML_DIR = SOURCE_BASE_DIR / "output/xml"

st.set_page_config(layout="wide")
st.title("Codiculum: Doxygen Parser & Chunker Test UI")


@st.cache_data
def get_xml_files(directory: Path) -> list[str]:
    """Finds all XML files in the specified directory."""
    if not directory.is_dir():
        return []

    return sorted(
        [
            f.name
            for f in directory.glob("*.xml")
            if f.is_file()
            and not f.name.endswith("_8cpp.xml")
            and not f.name.endswith("_8h.xml")
            and not f.name.endswith("_8td.xml")
            and not f.name.endswith("_8py.xml")
            and not f.name.endswith("_8inc.xml")
            and not f.name == "Doxyfile.xml"
        ]
    )


@st.cache_data
def load_and_chunk(xml_file_path: Path):
    """Loads Doxygen XML, parses it, and generates chunks."""
    if not xml_file_path.is_file():
        return None, None, f"Error: File not found - {xml_file_path}"

    try:
        parsed_data = parse_doxygen_xml_file(xml_file_path)
        if parsed_data is None:
            return None, None, f"Error parsing file {xml_file_path.name}"

        # Instantiate CodeChunker with the repo_dir from config
        chunker = CodeChunker(SOURCE_BASE_DIR)
        chunks = chunker.chunk(parsed_data)
        return parsed_data, chunks, None
    except Exception as e:
        return None, None, f"Error processing file {xml_file_path.name}: {e}"


# --- UI ---

xml_files = get_xml_files(DOXYGEN_XML_DIR)

if not xml_files:
    st.error(f"No XML files found in the specified directory: {DOXYGEN_XML_DIR}")
    st.stop()

selected_xml_file_name = st.sidebar.selectbox(
    "Select Doxygen XML File:",
    options=xml_files,
    index=0,  # Default to the first file in the list
    key="xml_selector",
)

if selected_xml_file_name:
    selected_xml_path = DOXYGEN_XML_DIR / selected_xml_file_name
    st.sidebar.info(f"Selected: `{selected_xml_path}`")

    # Load, parse, and chunk the data
    parsed_elements, chunks, error_message = load_and_chunk(selected_xml_path)

    if error_message:
        st.error(error_message)
        st.stop()

    if not parsed_elements:
        st.warning(f"No parsable elements found in {selected_xml_file_name}.")
        st.stop()

    # Map element IDs to chunks for easier lookup
    chunk_map = {chunk.metadata["id"]: chunk for chunk in chunks}

    st.sidebar.success(
        f"Parsed {len(parsed_elements)} elements and generated {len(chunks)} chunks."
    )

    # --- Element Selection ---
    element_options = {
        f"{elem.kind.capitalize()}: {elem.name} ({elem.id})": elem.id
        for elem in parsed_elements
    }
    selected_element_display_name = st.selectbox(
        "Select Code Element to View Chunk:", options=list(element_options.keys())
    )

    # --- Display Chunk ---
    if selected_element_display_name:
        selected_element_id = element_options[selected_element_display_name]
        selected_chunk = chunk_map.get(selected_element_id)

        st.subheader(f"Generated Chunk for: `{selected_element_display_name}`")
        if selected_chunk:
            st.markdown(f"""```cpp
{selected_chunk.text}
```""")  # Assuming C++ for now
            st.write("**Metadata:**")
            st.json(selected_chunk.metadata)
        else:
            st.warning(
                f"No chunk found for element ID: {selected_element_id}. This might be expected if the element type is not chunked (e.g., 'file')."
            )

else:
    st.info("Please select an XML file from the sidebar.")

# Add a way to clear the cache for debugging/development
if st.sidebar.button("Clear Cache"):
    st.cache_data.clear()
    st.rerun()
