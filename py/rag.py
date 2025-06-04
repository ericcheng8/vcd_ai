import faiss
import numpy as np
import subprocess
import re
import networkx as nx
from sentence_transformers import SentenceTransformer

def extract_ollama_model_from_script(script_path="training/train.ps1"):
  with open(script_path, 'r') as f:
    for line in f:
      if '$CUSTOM_MODEL_NAME' in line:
        match = re.search(r'\$CUSTOM_MODEL_NAME\s*=\s*"([^"]+)"', line)
        if match:
          return match.group(1)
  return "llama4"

class GraphRAGEngine:
  def __init__(self, signal_map, time_events, graph: nx.DiGraph):
    self.signal_map = signal_map
    self.time_events = time_events
    self.graph = graph
    self.documents = []
    self._prepare_documents()
    # self.model = SentenceTransformer("all-MiniLM-L6-v2") # fast & small mem footprint
    self.model = SentenceTransformer("all-mpnet-base-v2") # more accurate but larger mem footprint
    self.index = self._build_faiss_index()
    self.ollama_model = extract_ollama_model_from_script()

  def _prepare_documents(self):
    for symbol, info in self.signal_map.items():
      self.documents.append(f"{info['name']} is a {info['type']} with width {info['width']}")

    for time, changes in self.time_events.items():
      for change in changes:
        self.documents.append(f"At time {time}, signal {change['signal']} changed to {change['value']}")

  def _build_faiss_index(self):
    embeddings = self.model.encode(self.documents)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    self.embeddings = embeddings
    return index

  def _get_graph_context(self, question: str):
    relevant_context = []
    for node in self.graph.nodes:
      if node in question:
        children = list(self.graph.successors(node))
        parents = list(self.graph.predecessors(node))
        relevant_context.append(f"{node} is connected to: {', '.join(children + parents)}")

    return "\n".join(relevant_context)

  def answer(self, question: str, top_k=5):
    query_vec = self.model.encode([question])
    D, I = self.index.search(query_vec, top_k)
    retrieved = "\n".join([self.documents[i] for i in I[0]])

    graph_context = self._get_graph_context(question)

    prompt = f"""
Graph Context:
{graph_context}

Retrieved Data:
{retrieved}

Question:
{question}
"""

    print(prompt)

    result = subprocess.run(
      ["ollama", "run", self.ollama_model],
      input=prompt,
      text=True,
      capture_output=True
    )
    return result.stdout.strip()
