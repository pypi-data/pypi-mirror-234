import csv
import os
import argparse
import requests
import json
from .HTMLparsers import getSchiHubPDF, SciHubUrls
from .NetInfo import NetInfo
from urllib.parse import urljoin

parser = argparse.ArgumentParser(description='Download papers from Sci-Hub.')
parser.add_argument('--txt', type=str, required=True, help='The txt file containing the DOIs.')
args = parser.parse_args()

def setSciHubUrl():
    r = requests.get(NetInfo.SciHub_URLs_repo, headers=NetInfo.HEADERS)
    links = SciHubUrls(r.text)
    NetInfo.SciHub_URL = "https://sci-hub.ee"  
    print("\nUsing {} as Sci-Hub instance".format(NetInfo.SciHub_URL))

def saveFile(folder, file_name, content):
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(os.path.join(folder, file_name), 'wb') as f:
        f.write(content)

def getDownloadedDois(dwnl_dir):
    progress_file = os.path.join(dwnl_dir, 'progress.json')
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as file:
            return json.load(file)
    return []

def saveDownloadedDoi(dwnl_dir, doi):
    progress_file = os.path.join(dwnl_dir, 'progress.json')
    downloaded_dois = getDownloadedDois(dwnl_dir)
    downloaded_dois.append(doi)
    with open(progress_file, 'w') as file:
        json.dump(downloaded_dois, file)

def downloadPapers(doi_l, dwnl_dir):
    def URLjoin(*args):
        return "/".join(map(lambda x: str(x).rstrip('/'), args))

    setSciHubUrl()

    downloaded_dois = set(getDownloadedDois(dwnl_dir))
    if not os.path.exists(dwnl_dir):
        os.makedirs(dwnl_dir)

    csv_file = os.path.join(dwnl_dir, os.path.splitext(args.txt)[0] + '_doi_status.csv')
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['DOI', 'Modified DOI', 'Status'])

        for doi in doi_l:
            if doi in downloaded_dois:
                print(f"{doi} already downloaded.")
                writer.writerow([doi, doi.replace('/', '_'), 'True'])
                continue

            url = URLjoin(NetInfo.SciHub_URL, doi)
            r = requests.get(url, headers=NetInfo.HEADERS)
            content_type = r.headers.get('content-type')

            if 'application/pdf' in content_type:
                saveFile(dwnl_dir, doi.replace('/', '_') + '.pdf', r.content)
                print(f"Successfully downloaded {doi}")
                writer.writerow([doi, doi.replace('/', '_'), 'True'])
                saveDownloadedDoi(dwnl_dir, doi)
            elif 'application/pdf' not in content_type:
                pdf_url = getSchiHubPDF(r.text)
                if pdf_url is not None:
                    print(f"Extracted PDF URL: {pdf_url}")
                    
                    if not pdf_url.startswith('http'):
                        pdf_url = urljoin(NetInfo.SciHub_URL, pdf_url)

                    try:
                        r = requests.get(pdf_url, headers=NetInfo.HEADERS)
                        if 'application/pdf' in r.headers.get('content-type'):
                            saveFile(dwnl_dir, doi.replace('/', '_') + '.pdf', r.content)
                            print(f"Successfully downloaded {doi}")
                            writer.writerow([doi, doi.replace('/', '_'), 'True'])
                            saveDownloadedDoi(dwnl_dir, doi)
                        else:
                            print(f"Failed to download {doi}")
                            writer.writerow([doi, doi.replace('/', '_'), 'False'])
                    except Exception as e:
                        print(f"Error occurred: {e}")
                        writer.writerow([doi, doi.replace('/', '_'), 'Error'])
                else:
                    print(f"Failed to download {doi}")
                    writer.writerow([doi, doi.replace('/', '_'), 'False'])
        print("All tasks have been completed!")

def get_doi_l(doi_file):
    DOIs = []
    with open(doi_file) as file_in:
        DOIs = [line.strip() for line in file_in]
    return DOIs

folder_name = os.path.splitext(args.txt)[0]
DOIs = get_doi_l(args.txt)
downloadPapers(DOIs, folder_name)
