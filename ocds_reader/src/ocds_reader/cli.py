import argparse
import sys
from ocds_reader import reader as rdr
import uuid

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode',
                        default='query', choices=['batch', 'query', 'flow'], 
                        type=str.lower, required=True,
                        help='Mode to running read process ...')
    parser.add_argument('-y','--year', type=int)
    parser.add_argument('-k','--buyer_keyword', type=str.lower)
    parser.add_argument('-f','--file', 
                        default='',
                        type=str, help='File with keywords separed by new line to run in batch mode')
    return parser

def main():
    args = create_parser().parse_args()
    mode = args.mode
    year = args.year
    buyer_keyword = args.buyer_keyword
    filepath = args.file

    exec_uuid = uuid.uuid4()
    if mode=="batch":
        lines_count = 0
        with open(filepath, 'r') as fp:
            lines_count = len(fp.readlines())

        file = open(filepath, 'r')
        keywords = file.readlines()
        line = 1
        for keyword in keywords:
            processsing_info = "%s (%d/%d)" % (keyword.replace('\n', ''), line, lines_count)
            rdr.consume_ocds_headers(keyword, str(year), str(exec_uuid), processsing_info)
            line += 1

    if mode=="query":
        rdr.consume_ocds_headers(buyer_keyword, str(year), str(exec_uuid))