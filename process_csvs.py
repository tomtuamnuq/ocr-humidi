import os

import pandas as pd

from process_pdfs import results_dir

# here we assume first column is timestamp
# all other columns are numbers or floats
header = ['Time', 'Temp', 'Hum', 'DEWI']  # table column names


def process_csvs(res_dir: str, verbose_printing: bool = False) -> pd.DataFrame:
    """
    Create a pandas dataframe from the header-free csvs in `res_dir`.
    The first column must be a timestamp and the other columns numbers or floats
    :param res_dir: path to the directory with csvs
    :param verbose_printing: output processed files and NaN containing rows
    :return: combined pandas dataframe of all processed csvs
    """
    filenames = sorted(os.listdir(res_dir))
    frames: list[pd.DataFrame] = []
    for filename in filenames:
        if not filename.endswith(".csv"):
            print(f"{filename} no csv. Continue")
            continue
        if verbose_printing:
            print(f"Processing {filename}")
        # create dataframe with header
        df = pd.read_csv(os.path.join(res_dir, filename),
                         sep=',', header=None, usecols=[0, 1, 2, 3])
        df.columns = header
        df[header[0]] = pd.to_datetime(df[header[0]], dayfirst=True)
        for col in header[1:]:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        if verbose_printing:
            # to check csvs and repair manually
            print(df.loc[df.isnull().any(axis=1)])
        frames.append(df)
    return pd.concat(frames, ignore_index=True)


if __name__ == '__main__':
    data = process_csvs(results_dir)
    data.to_csv('data.csv')
