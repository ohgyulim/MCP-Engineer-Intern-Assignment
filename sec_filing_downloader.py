from pathlib import Path
import requests
import zipfile
import io


def download_sec_filing(cik: str, year: str, filing_type: str, output_dir_path: str) -> str:
    """
    Download the latest SEC filing data.

    Parameters
    ----------
    cik : str
        Central Index Key (CIK) of the company.
    year : str
        Target filing year.
    filing_type : str
        SEC filing form type.
    output_dir_path : str
        Saving file path.

    Returns
    -------
    return_path: str
        Path to the primary HTML document.

    Examples
    --------
    >>> path = download_sec_filing("0001018724", "2024", "8-K", "html/amzn_2024_8_k")
    """

    # example json_data url: https://data.sec.gov/submissions/CIK0001018724.json
    headers = {"User-Agent": "MyApp your.email@domain.com"}
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    res = requests.get(url, headers=headers)
    data = res.json()
    filings_recent = data["filings"]["recent"]
    
    # data is sorted By reportData
    accession_number = ""
    primary_document = ""
    for index, _filing_type in enumerate(filings_recent["form"]):
        report_date = filings_recent["reportDate"][index]
        if (_filing_type == filing_type and report_date.startswith(year)):
            accession_number = filings_recent["accessionNumber"][index]
            primary_document = filings_recent["primaryDocument"][index]
            break
        
    output_path = Path(output_dir_path)
    output_path.mkdir(parents=True, exist_ok=True)
    
    download_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_number.replace('-','')}/{accession_number}-xbrl.zip"
    res = requests.get(download_url, headers=headers)
    
    with zipfile.ZipFile(io.BytesIO(res.content)) as zf:
        zf.extractall(path=output_path)
    
    return_path = ""
    for path in output_path.glob("*"):
        if path.name == primary_document:
            return_path = path
    
    return return_path