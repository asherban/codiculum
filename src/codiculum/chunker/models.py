from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class Chunk:
    """
    Represents a chunk of code and associated metadata,
    formatted into a text block suitable for embedding.
    Aligns with LlamaIndex's expected Node structure (text + metadata).
    """
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    # Optional: Add properties for commonly accessed metadata for convenience?
    # @property
    # def filename(self) -> Optional[str]:
    #     return self.metadata.get('file_path')

    # @property
    # def start_line(self) -> Optional[int]:
    #     return self.metadata.get('start_line')