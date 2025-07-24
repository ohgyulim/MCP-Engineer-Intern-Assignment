from mcp.server.fastmcp import FastMCP
from html_to_pdf import html_to_pdf
from read_as_markdown import read_as_markdown
from sec_filing_downloader import download_sec_filing

mcp = FastMCP("SEC Filing Processor")

@mcp.tool()
def wrapped_sec_filing_downloader(cik, year, filing_type, output_dir_path):
    return download_sec_filing(cik, year, filing_type, output_dir_path)

@mcp.tool()
async def wrapped_html_to_pdf(input_file_path, output_file_path):
    return await html_to_pdf(input_file_path, output_file_path)

@mcp.tool()
def wrapped_read_as_markdown(input_file_path):
    return read_as_markdown(input_file_path)
