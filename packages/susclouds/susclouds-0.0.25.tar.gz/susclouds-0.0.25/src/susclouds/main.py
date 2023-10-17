"""
Script to create wordclouds for a given input file
(expects post text column name = "Full Text")
The script produces wordclouds per issue and word counts per brand in a new file
$ python top_words_and_clouds.py <filename> <stopwords> <phrases>
    filename - report file to be analysed
    stopwords - Excel file listing stopwords and phrases
    phrases - Excel file listing phrases that should be kept together
Output:
    *.png - word susclouds per issue
    netzero_wountcount_output.xlsx
"""

import argparse
import os
import re
import pandas as pd
from pathlib import Path
from typing import List
import time
import shutil

from susclouds.stopword_funcs import stopwords_from_file, update_stopwords, update_phrases
from susclouds.esg import wordcloud_by_sector_and_class_no_sector, wordcloud_all_sectors_by_class, wordcloud_all_sectors_all_class
from susclouds.netzero import wordcloud_nz

# Constants
DATA_ROOT = "./data"
start = time.time()


def _parse_args() -> argparse.Namespace:
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(description='Generate word susclouds')
    parser.add_argument('data',
                        help='input .xlsx files')
    parser.add_argument('action', choices=['create', 'update'],
                        help='input action command: create (wordclouds) or update (stop words / phrases)')

    parser.add_argument('--resource', choices=['stopwords', 'phrases'],
                        help='input directory containing .xlsx files')

    parser.add_argument('--type', choices=['Sector', 'Industry', 'Issue'],
                        help='which type of word cloud is to be created')
                        
    return parser.parse_args()


def main(args: argparse.Namespace):
    zippath = ""
    # open phrases and stopwords files
    source_file = os.path.abspath(Path(args.data).resolve())
    filename = os.path.basename(source_file)
    
    if args.action == 'update':
        if args.resource == 'stopwords':
            update_stopwords(source_file)
        else:
            update_phrases(source_file)
    
    elif args.action == 'create':
        phrases_df = pd.read_csv("phrases.csv")
        stopwords = stopwords_from_file(pd.read_csv("stopwords.csv"))

        if args.type == 'Issue':
            zippath = wordcloud_nz(source_file,
                                phrases_df,
                                stopwords,
                                Path("storage/" + filename.split(".")[0] + "/"))
        elif args.type == 'Sector':
            zippath = wordcloud_by_sector_and_class_no_sector(source_file,
                                                            phrases_df,
                                                            stopwords,
                                                            Path("storage/" + filename.split(".")[0] + "/"))
        elif args.type == 'Industry':
            zippath = wordcloud_all_sectors_all_class(source_file,
                                                    phrases_df,
                                                    stopwords,
                                                    Path("storage/" + filename.split(".")[0] + "/"))
            for c in ['Environmental', 'Social', 'Governance']:
                zippath = wordcloud_all_sectors_by_class(source_file,
                                                        phrases_df,
                                                        stopwords,
                                                        c,
                                                        Path("storage/" + filename.split(".")[0] + "/"))
        else:
            print("Invalid report type")
    else:
        print("Invalid instruction")
        
    if zippath != "":
    # make zip archive
        local_zip_name = 'storage/zips/' + filename.split('.')[0] + '_charts'
        zipname = shutil.make_archive(local_zip_name, 'zip', zippath)
        print(f"Clouds saved in: {local_zip_name}")

    end = time.time()

    total_time = end - start
    print("\n" + str(total_time))


if __name__ == '__main__':
    _args = _parse_args()
    main(_args)
