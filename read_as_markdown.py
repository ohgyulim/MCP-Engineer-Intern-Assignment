from typing import Union
from pathlib import Path

from docling.document_converter import DocumentConverter


def read_as_markdown(input_file_path: Union[str, Path]) -> str:
    """Convert PDF to MarkDown

    Parameters
    -------
    input_file_path : Union[str, Path]
        PDF file path

    Returns
    -------
    markdown : str
        Converted MarkDown Result

    Examples
    -------
    >>> input_file_path = "examples/example.pdf"
    >>> context = read_as_markdown(input_file_path)
    """
    
    input_file_path = Path(input_file_path)
    converter = DocumentConverter()
    try:
        markdown = converter.convert(input_file_path).document.export_to_markdown()
    except Exception as e:
        return f"[Docling Error]: {e}"
    
    return markdown
