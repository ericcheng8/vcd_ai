import networkx as nx

def build_knowledge_graph(signal_map):
  G = nx.DiGraph()

  for symbol, info in signal_map.items():
    path_parts = info['name'].split('.')
    for i in range(len(path_parts)):
      node = '.'.join(path_parts[:i+1])
      if not G.has_node(node):
        G.add_node(node, type='module' if i < len(path_parts) - 1 else 'signal')

      if i > 0:
        parent = '.'.join(path_parts[:i])
        G.add_edge(parent, node)

  return G
