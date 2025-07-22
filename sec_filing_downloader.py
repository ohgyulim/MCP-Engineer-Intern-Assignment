from pathlib import Path
import requests
import argparse
import zipfile
import io

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cik", type=str, required=True, help="CIK (Central Index Key)")
    parser.add_argument("-y", "--year", type=str, required=True, help="")
    parser.add_argument("-t", "--type", type=str, required=True, help="")
    parser.add_argument("-p", "--path", type=str, required=True, help="")

    return parser.parse_args()

def download_sec_filing(cik: str, year: str, filing_type: str, output_dir_path: str) -> str:
    # example json_data url: https://data.sec.gov/submissions/CIK0001018724.json
    headers = {"User-Agent": "MyApp your.email@domain.com"}
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    res = requests.get(url, headers=headers)
    data = res.json()
    filings_recent = data["filings"]["recent"]
    
    # data is sorted By reportData
    accession_number = ""
    primary_document = ""
    for index, type in enumerate(filings_recent["form"]):
        report_date = filings_recent["reportDate"][index]
        if (type == filing_type and report_date.startswith(year)):
            accession_number = filings_recent["accessionNumber"][index]
            primary_document = filings_recent["primaryDocument"][index]
            break
        
    output_path = Path(output_dir_path)
    output_path.mkdir(parents=True, exist_ok=True)
    
    download_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_number.replace("-","")}/{accession_number}-xbrl.zip"
    res = requests.get(download_url, headers=headers)
    
    with zipfile.ZipFile(io.BytesIO(res.content)) as zf:
        zf.extractall(path=output_path)
    
    return_path = ""
    for path in output_path.glob("*"):
        if path.name == primary_document:
            return_path = path;
    
    return return_path
    


if __name__ == "__main__":
    args = parse_args()
    cik = args.cik
    year = args.year
    filing_type = args.type
    output_dir_path = args.path
    
    download_sec_filing(cik, year, filing_type, output_dir_path)