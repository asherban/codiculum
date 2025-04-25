import logging

logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.DEBUG) # Removed basic config

def retrieve_source_snippet(filepath: str, start_line: int, end_line: int) -> str:
    """Retrieves a specific snippet of code from a file based on line numbers.

    Args:
        filepath: The absolute path to the source code file.
        start_line: The 1-based starting line number (inclusive).
        end_line: The 1-based ending line number (inclusive).

    Returns:
        The code snippet as a string.

    Raises:
        FileNotFoundError: If the filepath does not exist.
        ValueError: If start_line or end_line are invalid (e.g., <= 0, end < start).
        IndexError: If the line numbers are out of the file's bounds.
    """
    if start_line <= 0 or end_line <= 0:
        raise ValueError("Line numbers must be positive.")
    if end_line < start_line:
        raise ValueError(f"End line ({end_line}) cannot be less than start line ({start_line}).")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # logger.debug(f"Read {len(lines)} lines from {filepath}") # Removed print
    except FileNotFoundError:
        logger.error(f"Source file not found: {filepath}")
        raise
    except Exception as e:
        logger.error(f"Error reading source file {filepath}: {e}")
        raise

    if start_line > len(lines) or end_line > len(lines):
         # logger.error(f"Line numbers ({start_line}-{end_line}) out of range ({len(lines)} lines) for {filepath}") # Removed print
         raise IndexError(f"Line numbers ({start_line}-{end_line}) out of range for file {filepath} with {len(lines)} lines.")

    # Adjust to 0-based indexing for list slicing
    start_idx = start_line - 1
    end_idx = end_line # Slice goes up to, but does not include, end_idx
    snippet_lines = lines[start_idx:end_idx]
    # logger.debug(f"Sliced lines [{start_idx}:{end_idx}]: {snippet_lines!r}") # Removed print
    # print(f"DEBUG: Sliced lines [{start_idx}:{end_idx}]: {snippet_lines!r}") # REMOVED PRINT

    # Strip trailing newline from the last line, if present, but keep internal newlines
    if snippet_lines and snippet_lines[-1].endswith('\n'):
         # logger.debug(f"Stripping newline from last line: {snippet_lines[-1]!r}") # Removed print
         # print(f"DEBUG: Stripping newline from last line: {snippet_lines[-1]!r}") # REMOVED PRINT
         snippet_lines[-1] = snippet_lines[-1].rstrip('\n')
         # logger.debug(f"Last line after strip: {snippet_lines[-1]!r}") # Removed print
         # print(f"DEBUG: Last line after strip: {snippet_lines[-1]!r}") # REMOVED PRINT

    result = "".join(snippet_lines)
    # logger.debug(f"Joining snippet lines: {snippet_lines!r} -> {result!r}") # Removed print
    # print(f"DEBUG: Joining snippet lines: {snippet_lines!r} -> {result!r}") # REMOVED PRINT
    return result 