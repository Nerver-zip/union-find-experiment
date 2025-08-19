import pandas as pd
import glob
import os
import matplotlib.pyplot as plt

# ============ CONFIGURAÇÃO ============
PASTA_CSV = "./csv"
PASTA_RELATORIO = "./relatorio"
PASTA_IMAGENS = os.path.join(PASTA_RELATORIO, "imagens")
WORKLOAD_SELECIONADO = "find_heavy"  
IMPLEMENTACOES = ["uf_rand", "uf_rank"]
COLUNA_TEMPO = "time_us"
# ======================================

def plot_scatter_simples():
    os.makedirs(PASTA_IMAGENS, exist_ok=True)
    plt.figure(figsize=(10,6))

    for impl, cor in zip(IMPLEMENTACOES, ["red", "blue"]):
        padrao_arquivo = os.path.join(PASTA_CSV, f"{impl}_*.csv")
        arquivos_csv = glob.glob(padrao_arquivo)
        todos_df = []
        for arq in arquivos_csv:
            df = pd.read_csv(arq)
            df_filtrado = df[df['workload_label'] == WORKLOAD_SELECIONADO]
            if not df_filtrado.empty:
                todos_df.append(df_filtrado)
        if todos_df:
            df_concat = pd.concat(todos_df, ignore_index=True)
            plt.scatter(
                df_concat["num_nodes"],
                df_concat[COLUNA_TEMPO],
                color=cor,
                alpha=0.6,
                label=impl
            )

    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Número de nós", fontsize=14)
    plt.ylabel("Tempo de execução (µs, escala log)", fontsize=14)
    plt.title(f"Desempenho: UF-Rand vs UF-Rank - {WORKLOAD_SELECIONADO}", fontsize=16)
    plt.legend(title="Implementação", fontsize=15, title_fontsize=18, loc="upper left")  
    plt.grid(True, which="both", linestyle="--", alpha=0.5)

    nome_imagem = os.path.join(PASTA_IMAGENS, f"scatter_simples_{WORKLOAD_SELECIONADO}.png")
    plt.show()
    plt.savefig(nome_imagem, dpi=300)
    plt.close()
    print(f"Gráfico salvo em: {nome_imagem}")

if __name__ == "__main__":
    plot_scatter_simples()
