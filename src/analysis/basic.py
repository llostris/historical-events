import snap

from settings import DATA_DIR, GRAPH_GML_FILE, GRAPH_SNAP_FILE

if __name__ == "__main__":
    v = snap.TIntV()

    FIn = snap.TFIn(GRAPH_SNAP_FILE)
    graph = snap.TNEANet.Load(FIn)
    print len(list(graph.Nodes()))