# src/codiculum/doxygen_parser/models.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class CodeLocation:
    file: str
    start_line: Optional[int] = None # Corresponds to 'line' attribute in Doxygen XML
    end_line: Optional[int] = None   # Corresponds to 'bodyend' attribute in Doxygen XML

@dataclass
class CodeElement:
    id: str # Doxygen ID
    name: str
    kind: str # e.g., 'function', 'class', 'struct', 'variable', 'enum', 'define', 'file', 'namespace'
    language: str
    brief_description: Optional[str] = None
    detailed_description: Optional[str] = None # Can store signatures, parameters, etc. here if needed
    location: Optional[CodeLocation] = None
    template_params: Optional[str] = None # For C++ templates, e.g., "template <typename T>"

