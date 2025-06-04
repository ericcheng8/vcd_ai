import argparse
from vcd_parser import parse_vcd
from kg_builder import build_knowledge_graph
from rag import GraphRAGEngine

def main():
    parser = argparse.ArgumentParser(description="GraphRAG CLI for RTL VCD files")
    parser.add_argument("vcd_file", help="Path to .vcd file")
    parser.add_argument("question", help="Question about the RTL signals")
    args = parser.parse_args()

    signal_map, time_events = parse_vcd(args.vcd_file)
    graph = build_knowledge_graph(signal_map)
    rag = GraphRAGEngine(signal_map, time_events, graph)
    answer = rag.answer(args.question)
    print("\n📌 Answer:")
    print(answer)

if __name__ == "__main__":
    main()
