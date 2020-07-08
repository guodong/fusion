import networkx as nx
from z3 import *
import itertools
import threading
import multiprocessing
import time

file = 'Bics.gml'
set_param('parallel.enable', True)

def main(N, N1):
    s = Solver()
    ggml = nx.read_gml(file)

    g = nx.DiGraph()
    lid = 0
    for e in ggml.edges:
        code = []
        for i in range(0, N):
            code.append((Bool('u' + str(lid) + str(i)), Bool('v' + str(lid) + str(i))))
        lid = lid + 1
        g.add_edge(e[0], e[1], c=code)

        code1 = []
        for i in range(0, N):
            code1.append((Bool('u' + str(lid) + str(i)), Bool('v' + str(lid) + str(i))))
        lid = lid + 1
        g.add_edge(e[1], e[0], c=code1)

    print len(g.nodes)
    print len(g.edges)

    maxD = 0
    for n in g.nodes:
        if g.in_degree(n) > maxD:
            maxD = g.in_degree(n)

    print maxD
    return

    npaths = 30000
    paths = []
    out_edges = set([])
    for n1 in g.nodes:
        for n2 in g.nodes:
            if len(paths) == npaths:
                break
            if (n1 != n2):
                try:
                    path = nx.shortest_path(g, n1, n2)
                    paths.append(path)

                    # print path
                    edges = zip(path[:-1], path[1:])
                    out_edges = out_edges.union(edges)
                    codes = map(lambda x: g.get_edge_data(x[0], x[1])['c'], edges)
                    # print codes
                    for i in range(0, N):
                        s.add(Or([And(map(lambda x: x[i][0], codes)), And(map(lambda x: x[i][1], codes))]))
                    # s.add(Or([And(map(lambda x: x[1][0], codes)), And(map(lambda x: x[1][1], codes))]))


                except:
                    1
                    print 'nopath'

    print len(paths)
    nn = 0
    for n in g.nodes:
        if g.out_degree(n) > 1:
            edges = g.out_edges(n)

            for es in itertools.combinations(edges, 2):
                if es[0] in out_edges and es[1] in out_edges:
                    codes = map(lambda x: g.get_edge_data(x[0], x[1])['c'], es)
                    nn += 1
                    # s.add(Or([Not(Or([And(map(lambda y: y[0][0], codes)), And(map(lambda y: y[0][1], codes))])), Not(Or([And(map(lambda y: y[1][0], codes)), And(map(lambda y: y[1][1], codes))]))]))
                    # s.add(Or(map(lambda i: Not(Or([And(map(lambda y: y[i][0], codes)), And(map(lambda y: y[i][1], codes))])), range(0, N))))
                    s.add(Not(And(map(lambda i: Or([And(codes[0][i][0], codes[1][i][0]), And(codes[0][i][1], codes[1][i][1])]), range(0, N)))))
                else:
                    pass
                    # print 'not out port'
    m = s.check()
    print '----'
    print N
    print m

# main(2)

threads = []
for i in range(7, 9):
    thread = multiprocessing.Process(target=main, args=(i,i))
    threads.append(thread)
    thread.start()

# for t in threads:
#     t.start()

time.sleep(1000000)
