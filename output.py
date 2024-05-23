import pandas as pd
import numpy as np

def finalString(indices: list):
    df = pd.read_csv('./MLAlgo/ThousandCornellAbstracts.csv')
    # Initialize an empty list to store the strings
    strings = []
    # print(indices)
    # print(df.columns)
    # Iterate over the indices and construct the string for each row
    for idx in indices:
        row = df.iloc[idx]
        # Construct the string with title followed by hyperlink
        string = f"{row['title']}, <a href='https://arxiv.org/abs/{row['id']}'>{row['id']}</a>"
        # print(idx, string)
        strings.append(string)

    # Concatenate the strings with commas
    result_string = ', '.join(strings)

    return result_string

    