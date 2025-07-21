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
    markdown = converter.convert(input_file_path).document.export_to_markdown()
    return markdown


def save_markdown(markdown: str, output_file_path: Union[str, Path]):
    """Save string as MarkDown Format

    Parameters
    -------
    markdown : str
        Context to save as MarkDown
    output_file_path : Union[str, Path]
        Saving file path

    Examples
    -------
    >>> doc = "example"
    >>> saving_path = "examples/example.md"
    >>> save_markdown(doc, saving_path)
    """
    output_file_path = Path(output_file_path)
    output_folder = output_file_path.parent
    output_folder.mkdir(parents=True, exist_ok=True)
    file_name = f"{output_file_path.stem}.md"
    (output_folder / file_name).write_text(markdown, encoding="utf-8")


if __name__ == "__main__":
    saving_path = Path("markdown")
    for _path in Path("pdf").glob("*.pdf"):
        doc = read_as_markdown(_path)
        save_markdown(doc, saving_path / _path.stem)
        break