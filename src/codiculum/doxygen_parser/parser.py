# src/codiculum/doxygen_parser/parser.py
import os
from typing import List, Optional
from lxml import etree
from .models import CodeElement, CodeLocation

# TODO: Implement parsing functions 