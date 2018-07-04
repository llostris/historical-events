# Deprecated upon move to Python 3.0

# import networkx as nx
# import snap
#
# from settings import GRAPH_GML_FILE, GRAPH_SNAP_FILE
#
# if __name__ == "__main__":
#
#     graph_nx = nx.read_gml(GRAPH_GML_FILE)
#     print len(graph_nx.nodes())
#     print len(graph_nx.edges())
#
#     graph_snap = snap.TNEANet.New()
#
#     attributes = [ 'date', 'start_date', 'end_date']
#     for attr in attributes:
#         graph_snap.AddStrAttrN(attr)
#
#     for node in graph_nx.node:
#         print node, graph_nx.node[node]
#         graph_snap.AddNode(node)
#         for attr in attributes:
#             value = graph_nx.node[node][attr]
#             graph_snap.AddStrAttrDatN(node, value, attr)
#
#     for edge in graph_nx.edges():
#         print edge
#         graph_snap.AddEdge(edge[0], edge[1])
#
#     print len(list(graph_snap.Nodes()))
#     print len(list(graph_snap.Edges()))
#
#     FOut = snap.TFOut(GRAPH_SNAP_FILE)
#     graph_snap.Save(FOut)
#     FOut.Flush()