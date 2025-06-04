import streamlit as st
import subprocess
import os
from vcd_parser import parse_vcd
from kg_builder import build_knowledge_graph
from rag import GraphRAGEngine

st.title("RTL Signal Explorer (GraphRAG)")

uploaded_file = st.file_uploader("Upload a .vcd file", type="vcd")

if uploaded_file:
    vcd_path = "src/uploaded.vcd"
    with open(vcd_path, "wb") as f:
        f.write(uploaded_file.read())

    signal_map, time_events = parse_vcd(vcd_path)
    graph = build_knowledge_graph(signal_map)

    rag = GraphRAGEngine(signal_map, time_events, graph)

    question = st.text_input("Ask a question about the RTL signals")
    if question:
        answer = rag.answer(question)
        st.text_area("Answer", value=answer, height=300)

if st.button("Train / Refresh Ollama Model"):
    with st.spinner("Running model training..."):
        if os.name == "nt":  # Windows
            result = subprocess.run(
                ["powershell", "-ExecutionPolicy", "Bypass", "-File", "training/train.ps1"],
                capture_output=True, text=True
            )
        else:  # Unix/Linux/macOS
            result = subprocess.run(
                ["bash", "training/train.sh"],
                capture_output=True, text=True
            )
        st.code(result.stdout or result.stderr)
