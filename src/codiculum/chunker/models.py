import dataclasses
from typing import List, Optional


@dataclasses.dataclass
class Chunk:
    """
    Represents a chunk of code and its associated metadata,
    formatted according to the project's chunking strategy.
    """
    filename: str
    start_line: int
    end_line: int
    code_snippet: str
    imports: Optional[List[str]] = None
    brief_description: Optional[str] = None
    detailed_description: Optional[str] = None
    usage_examples: Optional[List[str]] = None
    is_partial: bool = False # Indicates if this chunk resulted from splitting a larger element

    def format_chunk_text(self) -> str:
        """Formats the chunk data into a single string for embedding."""
        # TODO: Implement formatting logic based on ChunkingStrategy.md
        # - Include filename, lines
        # - Add descriptions
        # - Add imports
        # - Add code
        # - Add examples
        # - Indicate if partial
        pass 