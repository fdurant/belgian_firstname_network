import argparse
import sys
import networkx as nx
from xlrd import open_workbook

def init():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inFileXls', dest='inFileXls', 
                        type=str,
                        help='input file with Belgian first names in MS Excel format',
                        required=True)
    parser.add_argument('--outFileGraphML', dest='outFileGraphML', 
                        type=str,
                        help='output file with Belgian first names in GraphML format',
                        required=True)
    global args
    args = vars(parser.parse_args())

def read_file(xlsFileName):
    wb = open_workbook(filename=xlsFileName)
    pass

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
