# -*- coding: utf-8 -*-
import argparse
import sys
import networkx as nx
from xlrd import open_workbook
from math import log
from nltk.util import bigrams
import community

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
    parser.add_argument('--startNumber', dest='startNumber', 
                        type=int, default=1,
                        help='rank number of the highest-ranked first name to include in output graph')
    parser.add_argument('--maxNrNames', dest='maxNrNames', 
                        type=int, default=100,
                        help='number of names to store in output network')
    parser.add_argument('--simThreshold', dest='simThreshold', 
                        type=float, default=0.2,
                        help='minimum inter-name similarity for a link to be created')
    parser.add_argument('--degreeThreshold', dest='degreeThreshold', 
                        type=float, default=1,
                        help='minimum degree required for a node to be included in the output graph')
    parser.add_argument('--rankThreshold', dest='rankThreshold', 
                        type=int, default=100,
                        help='all nodes below this rank are guaranteed to be included in the output graph')
    parser.add_argument('--bonusMultiplier', dest='bonusMultiplier', 
                        type=float, default=1.2,
                        help='the edge weights of the nodes below rankThreshold get multiplied with this bonus to increase their chances of survival')
    parser.add_argument('--outFileGraphML', dest='outFileGraphML', 
                        type=str,
                        help='output file with Belgian first names in GraphML format',
                        required=True)
    global args
    args = vars(parser.parse_args())
    print >> sys.stderr, args

def read_file(fileList):
    
    global G
    G = nx.Graph()

    # Internal mapping
    region2column = {1:1,
                     2:4,
                     3:7,
                     4:10}

    for fn in fileList:
        wb = open_workbook(filename=fn)
        sheet = wb.sheet_by_name(args['sheetName'])
        columnNumber = region2column[args['partOfCountry']]
        for i in range(args['startNumber'],
                       min(sheet.nrows,args['maxNrNames']+(args['startNumber']*len(fileList)))/len(fileList)):
            name = sheet.cell_value(i,columnNumber)
            freq = int(sheet.cell_value(i,columnNumber+1))
            rank = int(sheet.cell_value(i,columnNumber-1))
            # Give importance to first letter
            charBigrams = bigrams('_%s' % name)

            if not G.has_node(name):
                G.add_node(name, {'type': 'firstname', 'freq': freq, 'rank': rank, 'size': int(log(freq))*2})
                
            for cb in charBigrams:
                if not G.has_node(cb):
                    G.add_node(cb, {'type': 'charbigram'})
                if not G.has_edge(name, cb):
                    G.add_edge(name,cb)

def project_network():
    global nameNetwork
    nameNetwork = nx.bipartite.overlap_weighted_projected_graph(G, [n for n in G if G.node[n]['type']=='firstname'], jaccard=True)

    # Delete all edges that do not make the threshold
    print >> sys.stderr, "Deleting edges with too low weight in name network with %d nodes and %d edges... " % (nx.number_of_nodes(nameNetwork), nx.number_of_edges(nameNetwork)),
    for u,v,a in nameNetwork.edges(data=True):
        if int(G.node[u]['rank']) < args['rankThreshold'] or int(G.node[u]['rank']) < args['rankThreshold']:
            if a['weight'] * args['bonusMultiplier'] < args['simThreshold']:
                nameNetwork.remove_edge(u,v)
        else:
            if a['weight'] < args['simThreshold']:
                nameNetwork.remove_edge(u,v)
    print >> sys.stderr, "done"

    # Apply minimum degree
    print >> sys.stderr, "Deleting nodes with too low degree in name network with %d nodes and %d edges... " % (nx.number_of_nodes(nameNetwork), nx.number_of_edges(nameNetwork)),
    for node in list(nameNetwork):
        if nameNetwork.degree(node) < args['degreeThreshold']:
            if int(G.node[node]['rank']) > args['rankThreshold']:
                nameNetwork.remove_node(node)
            else:
                pass
#                print >> sys.stderr, "rank = %d not > %s" % (nameNetwork.node[node]['rank'], args['rankThreshold'])
        else:
            pass
#            print >> sys.stderr, "degree = %d not < %s" % (nameNetwork.degree(node), args['degreeThreshold'])

    print >> sys.stderr, "done"


    # Detect communities
    print >> sys.stderr, "Partitioning name network with %d nodes and %d edges ... " % (nx.number_of_nodes(nameNetwork), nx.number_of_edges(nameNetwork)),
    partition = community.best_partition(nameNetwork)
    print >> sys.stderr, "done"

    print >> sys.stderr, "Deleting unneeded attributes ...",
    for name in partition.keys():
        nameNetwork.node[name]['community'] = partition[name]
        nameNetwork.node[name]['label'] = name
        del nameNetwork.node[name]['type']
        del nameNetwork.node[name]['freq']
        del nameNetwork.node[name]['rank']
    print >> sys.stderr, "done"

def write_network():
    print >> sys.stderr, "Writing name network with %d nodes and %d edges ... " % (nx.number_of_nodes(nameNetwork), nx.number_of_edges(nameNetwork)),
    nx.write_graphml(nameNetwork, args['outFileGraphML'], 'utf-8')
    print >> sys.stderr, "done"

if __name__ == '__main__':
    init()
    read_file(args['inFileXls'])
    project_network()
    write_network()
