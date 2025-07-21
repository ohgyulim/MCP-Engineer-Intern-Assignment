from typing import Union
from pathlib import Path
import requests
import argparse



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cik", type=str, required=True, help="CIK (Central Index Key)")
    parser.add_argument("-y", "--year", type=int, required=True, help="")
    parser.add_argument("-t", "--type", type=str, required=True, help="")

    return parser.parse_args()
    

if __name__ == "__main__":
    args = parse_args()
    cik = args.cik
    year = args.year
    filing_type = args.type