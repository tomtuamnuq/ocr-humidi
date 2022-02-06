# ocr-humidi
Use case of OCRSpace API for scanned tabular data of humidity measurements.

Excessive humidity in an apartment required several weeks of measurements to analyze the situation with the aim of improving the indoor climate through targeted ventilation. 

Unfortunately, the measurement results could only be presented in paper form. Fortunately, [OCRSpace](https://ocr.space/OCRAPI) provides an API to easily parse PDF documents. The API returns the extracted text results in a JSON format.
With a free account one can send up to three pages at once. Since the measurements were printed on 22 pages I created a Python script for batch processing of each page, see `process_pdfs.py` for details. The script is optimized for tabular data.

The OCRSpace Engine 1 works quite well. However, problems occur when the pdf scan is not aligned perfectly. Nevertheless, only a little bit of data cleaning was necessary to make the csvs processable.

The script `process_csvs` combines the textual results into one pandas DataFrame. 

Final analyzation of the measurements is given in `Examination.ipynb`.
