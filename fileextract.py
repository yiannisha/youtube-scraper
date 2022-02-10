#!/usr/bin/env python3

''' A module to extract youtube data from a json file '''

import os
import sys
import json

import scrape

from typing import List

def jsonFileData(filepath: str) -> List:
    '''
    Returns data from a json file.
    '''

    data = []

    if os.path.isfile(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.loads(''.join(f.readlines()))
    else:
        raise FileNotFoundError(f'Cannot find file named: {filepath}')

    return data

if __name__ == '__main__':

    # parse arguments
    try:
        OUT_FILE = sys.argv[1]
    except:
        raise IndexError('No output csv file passed.\n')
    if not OUT_FILE.endswith('.csv') and not OUT_FILE.endswith('.xlsx'):
        raise ValueError('Output file must be CSV or XLSX.\n')

    try:
        filepath = sys.argv[2]
    except:
        raise FileNotFoundError('No json filepath passed.\n')
    if not filepath.endswith('.json'):
        raise ValueError('Input file must be JSON file.\n')

    # get data from file
    file_data = jsonFileData(filepath)

    # write data to output file
    if OUT_FILE.endswith('.csv'): scrape.exportCSV(file_data, OUT_FILE)
    if OUT_FILE.endswith('.xlsx'): scrape.exportXLSX(file_data, OUT_FILE)
