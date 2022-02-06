import json
import os

import requests

# to make things easy we just define global paths here
pdfs_dir = "pdfs"  # path to load pdfs from
raw_results_dir = "raw"  # path to save json formatted results per pdf
results_dir = "results"  # path to save csv results per pdf

with open(os.path.join('api_key.txt'), 'r') as key_file:
    # saved key from https://ocr.space/ocrapi/freekey as first line
    api_key = key_file.readline()

# see https://ocr.space/OCRAPI
payload = {'isOverlayRequired': False,
           'language': "ger",
           'apikey': api_key,
           'filetype': 'pdf',
           'detectOrientation': True,
           'scale': True,
           'isTable': True,
           'OCREngine': 1  # 2 did not work well
           }


def process_pdf(filename: str) -> str:
    """
    Sends the pdf to the OCR online service and gets the raw text from the response
    :param filename: pdf file in `pdfs_dir`
    :return: raw text of the http response content
    """
    # thanks to https://github.com/Zaargh/ocr.space_code_example/blob/
    # master/ocrspace_example.py
    with open(os.path.join(pdfs_dir, filename), 'rb') as file:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: file},
                          data=payload,
                          )
    return r.content.decode()


def process_text(raw_text: str) -> list[str]:
    """
    Parses each line in `raw_text` and adjusts chars as needed to get a csv format
    :param raw_text: string to parse lines from.
    :return: List of rows (strings) with tabular data in csv format.
    """
    results = list()
    text = raw_text
    for c in ('\r', '-', '—'):
        text = text.replace(c, '')
    text = text.replace(',', '.')
    lines = text.split('\n')
    for line in lines:
        words = line.split('\t')
        csv_string = ", ".join(words)
        results.append(csv_string + '\n')
    return results


def process_pdfs() -> None:
    """
    Processes each pdf in `pdfs_dir` with `process_pdf` and `process_text`.
    The response and parsed text are saved to disc in json and csv format.
    """
    filenames = sorted(os.listdir(pdfs_dir))
    for filename in filenames:
        if not filename.endswith(".pdf"):
            print(f"{filename} no pdf. Continue")
            continue
        print(f"Processing {filename}")
        ocr_string = process_pdf(filename)
        ocr_json = json.loads(ocr_string)
        with open(os.path.join(raw_results_dir, filename + ".json"), 'w') as file:
            json.dump(ocr_json, file)
        raw_text = ocr_json['ParsedResults'][0]['ParsedText']
        results = process_text(raw_text)
        with open(os.path.join(results_dir, filename + ".csv"), 'w') as file:
            file.writelines(results)


if __name__ == '__main__':
    process_pdfs()
