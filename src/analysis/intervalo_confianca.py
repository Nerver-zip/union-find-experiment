#!/usr/bin/env python3
import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

# ============ CONFIGURAÇÃO ============
PASTA_CSV = "./csv"
PASTA_RELATORIO = "./relatorio"
PASTA_IMAGENS = os.path.join(PASTA_RELATORIO, "imagens")
WORKLOAD_SELECIONADO = "union_heavy"  # escolha: "union_heavy" ou "find_heavy"
IMPLEMENTACOES = ["uf_rand", "uf_rank"]
COLUNA_TEMPO = "time_us"
# ======================================

def plot_mean_ic():
    os.makedirs(PASTA_IMAGENS, exist_ok=True)
    todos_df = []

    for impl in IMPLEMENTACOES:
        padrao_arquivo = os.path.join(PASTA_CSV, f"{impl}_*.csv")
        arquivos_csv = glob.glob(padrao_arquivo)
        for arq in arquivos_csv:
            try:
                df = pd.read_csv(arq)
                df_filtrado = df[df['workload_label'] == WORKLOAD_SELECIONADO]
                if not df_filtrado.empty:
                    df_filtrado = df_filtrado.copy()
                    df_filtrado['impl'] = impl
                    todos_df.append(df_filtrado)
            except Exception as e:
                print(f"Erro ao ler '{arq}': {e}")

    if not todos_df:
        print(f"Nenhum dado encontrado para o workload {WORKLOAD_SELECIONADO}")
        return

    df_completo = pd.concat(todos_df, ignore_index=True)

    # Agrupar por implementação e tamanho do input
    medias = df_completo.groupby(['impl', 'num_nodes'])[COLUNA_TEMPO].mean().reset_index()
    desvio = df_completo.groupby(['impl', 'num_nodes'])[COLUNA_TEMPO].std().reset_index()
    n_counts = df_completo.groupby(['impl', 'num_nodes'])[COLUNA_TEMPO].count().reset_index()

    # Calcula IC 95%
    ic95 = 1.96 * desvio[COLUNA_TEMPO] / np.sqrt(n_counts[COLUNA_TEMPO])

    medias['ic95'] = ic95

    # Configurações visuais
    sns.set(style="whitegrid")
    plt.figure(figsize=(20, 12))
    cores = {'uf_rand':'#FF3333', 'uf_rank':'#3333FF'}

    for impl in IMPLEMENTACOES:
        df_plot = medias[medias['impl'] == impl]
        plt.errorbar(
            df_plot['num_nodes'],
            df_plot[COLUNA_TEMPO],
            yerr=df_plot['ic95'],
            fmt='o-',
            color=cores[impl],
            ecolor='black',  # destaque no IC
            elinewidth=2,
            capsize=5,
            label=impl
        )

    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel("Tamanho do input")
    plt.ylabel("Tempo médio (µs) ± IC 95% [escala log]")
    plt.title(f"Média ± IC 95% - Workload: {WORKLOAD_SELECIONADO}")

    plt.legend(title="Implementação", loc='upper left', bbox_to_anchor=(1.02,1), fontsize=12, title_fontsize=14)

    plt.tight_layout()
    nome_imagem = os.path.join(PASTA_IMAGENS, f"mean_ic_{WORKLOAD_SELECIONADO}.png")
    plt.savefig(nome_imagem, dpi=300)
    plt.show()
    plt.close()
    print(f"Gráfico salvo em: {nome_imagem}")

if __name__ == "__main__":
    plot_mean_ic()

