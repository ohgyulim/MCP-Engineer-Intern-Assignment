from pathlib import Path
import pandas as pd
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
    
    # 1. request for filing data
    data = request_for_data(url, headers)

    # 2. process data for downloading files
    processed_data = process_data(data, filing_type, year)
    accession_number = processed_data["accessionNumber"]
    primary_document = processed_data["primaryDocument"]
    
    # 3. download and extract files
    output_path = download_and_extract(output_dir_path, headers, cik, accession_number)
    
    # 4. return result path
    result_path = find_path(output_path, primary_document)
    
    return result_path


def request_for_data(url: str, headers: dict) -> dict:
    """
    Request SEC filing data from the given URL.

    Parameters
    ----------
    url : str
        The URL to request SEC filing data from.
    headers : dict
        HTTP headers for the request.

    Returns
    -------
    dict
        JSON response data containing SEC filing information.

    Examples
    --------
    >>> headers = {"User-Agent": "MyApp your.email@domain.com"}
    >>> url = "https://data.sec.gov/submissions/CIK0001018724.json"
    >>> data = request_for_data(url, headers)
    """
    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        data = res.json()
        return data
    except requests.RequestException as e:
        print(f"[Request Error]: {e}")
        raise
    
def process_data(data:dict, filing_type: str, year: str) -> dict:
    """
    Process SEC filing data to find the target filing information.

    Parameters
    ----------
    data : dict
        Raw SEC data retrieved from SEC API.
    filing_type : str
        SEC filing form type.
    year : str
        Target filing year.

    Returns
    -------
    dict
        accessionNumber, primaryDocument data

    Examples
    --------
    >>> processed_data = process_data(data, "8-K", "2024")
    """
    filings_recent_data = pd.DataFrame(data["filings"]["recent"])
    
    if len(filings_recent_data) == 0:
        raise
    
    required_columns = ["reportDate", "form", "accessionNumber", "primaryDocument"]
    if not set(required_columns).issubset(set(filings_recent_data.columns)):
        raise ValueError("[Value Error]: Required column(s) not in SEC data.")
    
    filings_recent_data = (
        pd.DataFrame(data["filings"]["recent"])
        .assign(
            reportDate=lambda d: pd.to_datetime(d["reportDate"]),
            reportYear=lambda d: d["reportDate"].dt.year,
        )
    )
    target_row = (
        filings_recent_data
        .query(f"form == '{filing_type}' and reportYear == {year}")
        .sort_values("reportDate", ascending=False)
        .iloc[0]
    )

    accession_number = target_row["accessionNumber"]
    primary_document = target_row["primaryDocument"]
    return {"accessionNumber": accession_number, "primaryDocument": primary_document}


def download_and_extract(output_dir_path: str, headers: dict, cik: str, accession_number: str) -> Path:
    """
    Download and extract SEC filing ZIP file.

    Parameters
    ----------
    output_dir_path : str
        Extracted path.
    headers : dict
        HTTP headers for the request.
    cik : str
        Central Index Key (CIK) of the company.
    accession_number : str
        SEC filing accession number.

    Returns
    -------
    Path
        Path object pointing to the extraction directory.

    Examples
    --------
    >>> headers = {"User-Agent": "MyApp your.email@domain.com"}
    >>> path = download_and_extract("output/", headers, "0001018724", "0001018724-24-000123")
    """
    output_path = Path(output_dir_path)
    output_path.mkdir(parents=True, exist_ok=True)
    download_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_number.replace('-','')}/{accession_number}-xbrl.zip"
    try:
        res = requests.get(download_url, headers=headers)
        res.raise_for_status()
        with zipfile.ZipFile(io.BytesIO(res.content)) as zf:
            zf.extractall(path=output_path)
        return output_path
    except requests.RequestException as e:
        print(f"[Request Error]: {e}")
        raise
    except:
        print("[Zip Error]: Error for zipfile extract process.")
        raise
    
def find_path(output_path: Path, primary_document: str) -> str:
    """
    Find the path to the primary document file.

    Parameters
    ----------
    output_path : Path
        Saving file path.
    primary_document : str
        Primary document name.

    Returns
    -------
    path: str
        Saving file path.

    Examples
    --------
    >>> path = find_path(Path("output/"), "primary_doc.htm")
    >>> print(path)
    """
    for path in output_path.glob("*"):
        if path.name == primary_document:
            return path
    raise