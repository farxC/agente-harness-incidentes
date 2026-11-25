from langchain.messages import AIMessage, HumanMessage, ToolMessage


def exibir_grafo(agente) -> None:
    """Exibe no terminal a estrutura estática do grafo."""
    grafo = agente.get_graph()

    print("\n=== GRAFO DO AGENTE ===")
    print(grafo.draw_ascii())

    print("Conexões:")
    for aresta in grafo.edges:
        tipo = "condicional" if aresta.conditional else "direta"
        print(f"  {aresta.source} -> {aresta.target} ({tipo})")


def perguntar(
    agente,
    texto: str,
    thread_id: str = "incidente-pagamentos-001",
) -> str:
    """Executa o agente, exibe seu fluxo e devolve a resposta final."""
    configuracao = {"configurable": {"thread_id": thread_id}}
    resposta_final = ""

    print("\n=== FLUXO DE EXECUÇÃO ===")
    print(f"[entrada] {texto}")

    for atualizacao in agente.stream(
        {"messages": [HumanMessage(content=texto)]},
        configuracao,
        stream_mode="updates",
    ):
        for nome_no, dados in atualizacao.items():
            print(f"\n[nó] {nome_no}")

            for mensagem in dados.get("messages", []):
                if isinstance(mensagem, AIMessage):
                    if mensagem.tool_calls:
                        for chamada in mensagem.tool_calls:
                            print(f"  ferramenta solicitada: {chamada['name']}")
                            print(f"  argumentos: {chamada['args']}")
                    elif mensagem.content:
                        resposta_final = str(mensagem.content)
                        print("  resposta final produzida pelo modelo")

                elif isinstance(mensagem, ToolMessage):
                    print(f"  resultado da ferramenta: {mensagem.content}")

    return resposta_final
