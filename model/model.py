from itertools import count

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self.grafo=nx.Graph()
        self.grafo_filtrato=nx.Graph()
        self.aeroporti= DAO.get_allAirports()
        self.idMap_Aeroporti={}
        for a in self.aeroporti:
            self.idMap_Aeroporti[a.ID]=a

    def add_nodi(self):
        self.grafo.add_nodes_from(self.aeroporti)

    def add_archi_pesati(self):
        lista_voli=DAO.get_allFlights()
        for tupla in lista_voli:
            if self.grafo.has_edge(self.idMap_Aeroporti[tupla[0]],
                                   self.idMap_Aeroporti[tupla[1]]):
                self.grafo[self.idMap_Aeroporti[tupla[0]]][self.idMap_Aeroporti[tupla[1]]]["somma"]+=tupla[2]
                self.grafo[self.idMap_Aeroporti[tupla[0]]][self.idMap_Aeroporti[tupla[1]]]["count"]+=tupla[3]
                somma= self.grafo[self.idMap_Aeroporti[tupla[0]]][self.idMap_Aeroporti[tupla[1]]]["somma"]
                conto=self.grafo[self.idMap_Aeroporti[tupla[0]]][self.idMap_Aeroporti[tupla[1]]]["count"]
                media=somma/conto
                self.grafo[self.idMap_Aeroporti[tupla[0]]][self.idMap_Aeroporti[tupla[1]]]["media"]=media
            else:
                self.grafo.add_edge(self.idMap_Aeroporti[tupla[0]],self.idMap_Aeroporti[tupla[1]],
                                    somma=tupla[2], count=tupla[3], media=tupla[2]/tupla[3])

    def crea_grafo(self):
        self.add_nodi()
        self.add_archi_pesati()

    def output_grafo(self, distanza):
        self.crea_grafo()
        for i,j in self.grafo.edges:
            if self.grafo[i][j]["media"]>distanza:
                self.grafo_filtrato.add_node(i)
                self.grafo_filtrato.add_node(j)
                self.grafo_filtrato.add_edge(i,j,media=self.grafo[i][j]["media"])
        stringa=(f"Numero totale di nodi: {len(self.grafo.nodes)}\n"
                 f"Numero totale di archi: {len(self.grafo_filtrato.edges)}\n")
        archi = self.grafo_filtrato.edges
        for i, j in archi:
            stringa=stringa+f"arco: {i.ID}-{j.ID} distanza media:{self.grafo_filtrato[i][j]["media"]}\n"
        return stringa

