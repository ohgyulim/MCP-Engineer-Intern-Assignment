from typing import Union
from pathlib import Path

from playwright.async_api import async_playwright


async def html_to_pdf(input_file_path: Union[str, Path], output_file_path: Union[str, Path]) -> str:
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
    abs_file_path = input_file_path.absolute().as_uri()
    
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(abs_file_path)
            await page.pdf(path=output_file_path)
            await browser.close()
    except Exception as e:
        print(f"[Playwright Error]: {e}")
        raise
        
    return str(output_file_path)