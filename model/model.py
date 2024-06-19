import copy

import networkx as nx

from database.DAO import DAO



class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._idMap = {}
        self._metodi = DAO.getAllMethods()

    def _creaGrafo(self, metodo, anno, s):
        self._nodes = DAO.getAllNodes(metodo, anno)
        for p in self._nodes:
            self._idMap[p.product_number] = p
            self._grafo.add_node(p)
        s = 1 + s
        archi = DAO.getAllEdges(metodo, anno, s)
        for a in archi:
            p1 = self._idMap[a[0]]
            p2 = self._idMap[a[1]]
            self._grafo.add_edge(p1, p2)


    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)


    def prodotti_redditizzi(self):
        prodotti = []
        nodi = list(self._grafo.nodes)
        nodi.sort(key=lambda x: x.ricavi_tot)
        for n in nodi:
            prodotti.append((n, self._grafo.in_degree(n)))

        prodotti.sort(key=lambda x: x[1], reverse=True)
        return prodotti[:5]

    def cammino(self):
        self._bestPath = []
        self._bestLunghezza = 0
        nodi = self._grafo.nodes
        for n in nodi:
            if self._grafo.in_degree(n) == 0:
                self._ricorsione(n, [])

        return self._bestPath, self._bestLunghezza

    def _ricorsione(self, n, parziale):
        if len(parziale) > 0:
            ultimo_nodo = parziale[-1][1]
        if len(parziale) > self._bestLunghezza and self._grafo.out_degree(ultimo_nodo) == 0:
            self._bestLunghezza = len(parziale)
            self._bestPath = copy.deepcopy(parziale)

        vicini = self._grafo.successors(n)
        for v in vicini:
            if self.filtroNodi(v, parziale) and self.filtroArchi(n, v, parziale):
                parziale.append((n, v))
                self._ricorsione(v, parziale)
                parziale.pop()

    def filtroNodi(self, v, parziale):
        for e in parziale:
            if e[0] == v or e[1] == v:
                return False
        return True

    def filtroArchi(self, n, v, parziale):
        for e in parziale:
            if e == (n, v) or e == (v, n):
                return False
        return True
