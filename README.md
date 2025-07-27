## MCP SEC Filing Tools

### Overview

This repository implements three Model Context Protocol (MCP) tools for working with SEC EDGAR filings:

1. `sec_filing_downloader`: Downloads the latest SEC filing (e.g., 10-K) for a given CIK and year.
2. `html_to_pdf`: Converts an HTML SEC filing document to PDF.
3. `read_as_markdown`: Converts an HTML SEC filing document to Markdown text.

These tools are intended to run in a containerized environment and integrate with Claude Desktop.

---

### Installation

### Not using Docker?

You can install and run the tools directly using the following steps:

### Clone Repo
```bash
git clone https://github.com/ohgyulim/MCP-Engineer-Intern-Assignment.git
cd MCP-Engineer-Intern-Assignment
```


### Adding MCP to your python project

Install the required dependencies:

```bash
pip install fastmcp docling playwright requests
playwright install --with-deps
```

---

### Quickstart (Using Docker)

### Pull the Docker image

```bash
docker pull ohgyulim/sec-filing-tool:v1.8
```


---


### Running Server

#### Development Mode

Run locally (non-Docker):

```bash
fastmcp run main.py:mcp --transport stdio
```



### Claude Desktop Integration

Use the following `claude_desktop_config.json`:

### Without Docker
```json
{
  "mcpServers": {
    "SEC-TOOL": {
      "command": "uv",
      "args": [
        "run",
        "{your_path}/main.py"
      ]
    }
  }
}
```
**Note: Replace {your_path} with the absolute path to your main.py file.**


### With Docker
```json
{
  "mcpServers": {
    "SEC-TOOL-DOCKER": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "--name",
        "sec-filing-container",
        "ohgyulim/sec-filing-tool:v1.8",
        "fastmcp",
        "run",
        "main.py:mcp",
        "--transport",
        "stdio"
      ]
    }
  }
}
```

---


### Prompt Template

You can use all three tools in a single natural language prompt like this in Claude Desktop:

Template variables:
- `{filing_type}`: Filing type (e.g., 10-K, 8-K, 10-Q)
- `{company name or CIK}`: Company name or CIK number
- `{year}`: Filing year (only 2021–2025 supported)
- `{your_output_path}`: Output folder path under /app/html

### Template
```
Please download the latest **{filing-type}** filing from **{company name or cik}** in **{year}**. Save it in the folder **{your_path}**.
Then, convert the main HTML file in that folder to PDF and save it in **{your_path}**/new_{comapny}_{year}_{filing_type}.pdf.
Finally, extract the content of that HTML file as markdown and Show me markdown.
```


### Example
```
Please download the latest 10-K filing from Amazon (CIK 0001018724) in 2024. Save it in the folder /app/html/amzn_2024_10_k.
Then, convert the main HTML file in that folder to PDF and save it in /app/pdf/new_{comapny}_{year}_{filing_type}.pdf.
Finally, extract the content of that HTML file as markdown and Show me markdown.
```

**Note: All paths must be under /app/ since the tools are containerized.**




### Documentation

* [SEC EDGAR API](https://www.sec.gov/edgar/sec-api-documentation)
* [Fast MCP](https://gofastmcp.com/getting-started/welcome)
* [Playwright Python](https://playwright.dev/python/)
* [Model Context Protocol Docs](https://modelcontextprotocol.io)
