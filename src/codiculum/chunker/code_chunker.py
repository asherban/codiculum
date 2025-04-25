# Contains the main logic for chunking code based on Doxygen output.

import logging
from pathlib import Path
# Use List directly if Python >= 3.9
from typing import List # , Dict, Any Removed unused imports
from .models import Chunk
from .source_retriever import retrieve_source_snippet
from ..doxygen_parser.models import CodeElement # , CodeLocation Removed unused import

# Configure basic logging - Reset to INFO
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG) # Remove forced level

def format_element_to_chunk(element: CodeElement, source_snippet: str) -> Chunk:
    """
    Formats a parsed code element and its source snippet into a Chunk object
    suitable for LlamaIndex Nodes (text + metadata).

    Args:
        element: The parsed CodeElement from Doxygen data.
        source_snippet: The corresponding source code snippet.

    Returns:
        A Chunk object populated with data from the element and snippet.

    Raises:
        ValueError: If the element's location information is missing.
    """
    if not element.location or not element.location.file:
        raise ValueError(f"Cannot create chunk for element '{element.id}' without location info.")

    # Construct the text content exactly as defined in the unit test
    # Note: We assume 'python' for the code block language for simplicity here.
    # A more robust solution might inspect the file extension.
    expected_text = f"""Brief: {element.brief_description}
Detailed: {element.detailed_description}

Code:
```python
{source_snippet}```"""

    # Populate metadata as expected by the unit test
    metadata = {
        "id": element.id,
        "name": element.name,
        "kind": element.kind,
        "file_path": element.location.file,
        "start_line": element.location.start_line,
        "end_line": element.location.end_line,
        "brief_description": element.brief_description or "", # Ensure not None
        "detailed_description": element.detailed_description or "", # Ensure not None
        # Note: source_snippet is now part of the main 'text' field
    }

    return Chunk(
        text=expected_text,
        metadata=metadata
    )


def create_chunks_from_doxygen(
    parsed_data: List[CodeElement], # Corrected type hint
    src_base_path: Path
) -> List[Chunk]:
    """
    Orchestrates the creation of code chunks from parsed Doxygen data.

    Args:
        parsed_data: A list of CodeElement objects representing parsed code elements
                     (functions, classes, etc.) from Doxygen XML.
        src_base_path: The root path of the source code directory.

    Returns:
        A list of Chunk objects ready for embedding.
    """
    chunks: List[Chunk] = []
    processed_count = 0
    error_count = 0

    logger.info(f"Starting chunk creation for {len(parsed_data)} parsed elements.")

    for element in parsed_data:
        # ---- REMOVE DEBUGGING ----
        # logger.debug(f"Processing element: ID={element.id}, Name={element.name}, Kind={element.kind}")
        # if hasattr(element, 'location'):
        #     logger.debug(f"  Element location object: {element.location!r}")
        #     if element.location:
        #         logger.debug(f"  Location attributes: file={getattr(element.location, 'file', 'N/A')}, start={getattr(element.location, 'start_line', 'N/A')}, end={getattr(element.location, 'end_line', 'N/A')}")
        #     else:
        #         logger.debug(f"  Element location is None.")
        # else:
        #     logger.debug(f"  Element has no 'location' attribute.")
        # ---- REMOVE DEBUGGING ----

        if not element.location or not element.location.file or element.location.start_line is None:
            logger.warning(f"Skipping element '{element.name}' due to missing or incomplete location information.")
            error_count += 1
            continue

        try:
            # Correct function call for retriever
            full_file_path = src_base_path / element.location.file
            if not full_file_path.is_file():
                logger.error(f"Source file not found at calculated path: {full_file_path}. Skipping element '{element.name}'.")
                error_count += 1
                continue

            # Doxygen line numbers are usually 1-based
            start_line = element.location.start_line
            end_line = element.location.end_line
            # Add check for None values, although parser should handle this ideally
            if start_line is None or end_line is None:
                 logger.warning(f"Skipping element '{element.name}' due to missing start/end line numbers.")
                 error_count += 1
                 continue

            snippet = retrieve_source_snippet(
                filepath=str(full_file_path), # Pass absolute path as string
                start_line=start_line,
                end_line=end_line
            )

            # Correct function call for formatter (local function)
            chunk = format_element_to_chunk(element, snippet)
            chunks.append(chunk)
            processed_count += 1

        except FileNotFoundError: # Should be caught by the check above, but keep as fallback
            logger.error(f"Source file not found for element '{element.name}': {src_base_path / element.location.file}. Skipping.")
            error_count += 1
        except (ValueError, IndexError) as e:
            logger.error(f"Error retrieving snippet for element '{element.name}' in '{element.location.file}': {e}. Skipping.")
            error_count += 1
        except Exception as e:
            # Catch potential errors during formatting or unexpected issues
            logger.error(f"Failed to create chunk for element '{element.name}': {e}", exc_info=True) # Include traceback
            error_count += 1

    logger.info(f"Chunk creation finished. Processed: {processed_count}, Errors/Skipped: {error_count}, Total Chunks: {len(chunks)}")
    return chunks


# def chunk_code(): # Placeholder - keep for now
#     pass 