# -*- coding: utf-8 -*-
import argparse
import sys
import networkx as nx
from xlrd import open_workbook

def init():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inFileXls', dest='inFileXls', 
                        type=str, nargs='+',
                        help='input file(s) with Belgian first names in MS Excel format',
                        required=True)
    parser.add_argument('--sheetName', dest='sheetName', 
                        type=str, default='1995-2015',
                        help='name of the sheet - i.e. year - of interest, e.g. 2000 (default is 1995 through 2015)')
    parser.add_argument('--partOfCountry', dest='partOfCountry', 
                        type=int, default=1,
                        help='1 = whole of Belgium (DEFAULT); 2 = Brussels only; 3=Flanders only; 4=Wallonia only)')
    parser.add_argument('--outFileGraphML', dest='outFileGraphML', 
                        type=str,
                        help='output file with Belgian first names in GraphML format',
                        required=True)
    global args
    args = vars(parser.parse_args())
    print args

def read_file(fileList):
    
    # Internal mapping
    region2column = {1:1,
                     2:4,
                     3:7,
                     4:10}

    for fn in fileList:
        wb = open_workbook(filename=fn)
        sheet = wb.sheet_by_name(args['sheetName'])
        columnNumber = region2column[args['partOfCountry']]
        
        // CONTINUE HERE

def build_network():
    pass

def project_network():
    pass

def write_network():
    pass

if __name__ == '__main__':
    init()
    read_file(args['inFileXls'])
    build_network()
    project_network()
    write_network()
