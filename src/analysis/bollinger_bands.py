import pandas as pd
import glob
import os
import matplotlib.pyplot as plt

# ============ CONFIGURAÇÃO ============
PASTA_CSV = "./csv"
PASTA_RELATORIO = "./relatorio"
PASTA_IMAGENS = os.path.join(PASTA_RELATORIO, "imagens")
WORKLOAD_SELECIONADO = "union_heavy"  # escolha: "union_heavy" ou "find_heavy"
IMPLEMENTACOES = ["uf_rand", "uf_rank"]
COLUNA_TEMPO = "time_us"
# ======================================

def plot_bollinger_bands():
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
        if not todos_df:
            continue

        df_concat = pd.concat(todos_df, ignore_index=True)

        # Pontos individuais
        plt.scatter(
            df_concat["num_nodes"],
            df_concat[COLUNA_TEMPO],
            color=cor,
            alpha=0.3,
            label=f"{impl} execuções"
        )

        # Estatísticas por tamanho
        stats = df_concat.groupby("num_nodes")[COLUNA_TEMPO].agg(["mean","std"]).reset_index()
        stats["upper"] = stats["mean"] + 2*stats["std"]
        stats["lower"] = stats["mean"] - 2*stats["std"]

        # Linhas da média
        plt.plot(
            stats["num_nodes"],
            stats["mean"],
            color=cor,
            linewidth=2,
            label=f"{impl} média"
        )
        # Bandas ±2 desvios
        plt.fill_between(
            stats["num_nodes"],
            stats["lower"],
            stats["upper"],
            color=cor,
            alpha=0.2
        )

    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Número de nós (escala log)", fontsize=14)
    plt.ylabel("Tempo de execução (µs, escala log)", fontsize=14)
    plt.title(f"Desempenho: UF-Rand vs UF-Rank com bandas ±2 desvios - {WORKLOAD_SELECIONADO}", fontsize=16)
    plt.legend(fontsize=12, title_fontsize=13)
    plt.grid(True, which="both", linestyle="--", alpha=0.5)

    nome_imagem = os.path.join(PASTA_IMAGENS, f"bollinger_{WORKLOAD_SELECIONADO}.png")
    plt.savefig(nome_imagem, dpi=300)
    plt.show()
    plt.close()
    print(f"Gráfico salvo em: {nome_imagem}")

if __name__ == "__main__":
    plot_bollinger_bands()
