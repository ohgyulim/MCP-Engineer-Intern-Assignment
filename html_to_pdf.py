from typing import Union
from pathlib import Path

from playwright.sync_api import sync_playwright


def html_to_pdf(input_file_path: Union[str, Path], output_file_path: Union[str, Path]):
    """Convert HTM/HTML to PDF

    Parameters
    -------
    input_file_path : Union[str, Path]
        HTM/HTML file path
    output_file_path : Union[str, Path]
        Saving file path

    Examples
    -------
    >>> input_file_path = "examples/example.html"
    >>> output_file_path = "examples/example.pdf"
    >>> html_to_pdf(input_file_path, output_file_path)
    """
    input_file_path = Path(input_file_path)
    output_file_path = Path(output_file_path)
    output_file_path.parent.mkdir(parents=True, exist_ok=True)
    abs_file_path = input_file_path.absolute().as_uri();
    
    with sync_playwright () as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(abs_file_path)
        page.pdf(path=output_file_path)
        browser.close()
        


def check_valid_html_ext(file_path: Union[str, Path]) -> bool:
    html_file_ext = [".html", ".htm"]
    for ext in html_file_ext:
        if file_path.suffix.lower() == ext:
            return True
    else:
        return False


if __name__ == "__main__":
    saving_path = "pdf_from_html"
    for html_file_path in Path("html").glob("**/*"):
        if check_valid_html_ext(html_file_path):
            print(html_file_path)
            output_pdf_path = f"{saving_path}/new_{html_file_path.stem}.pdf"
            html_to_pdf(html_file_path, output_pdf_path)