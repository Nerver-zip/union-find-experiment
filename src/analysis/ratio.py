#!/usr/bin/env python3
import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
import seaborn as sns

# ============ CONFIGURAÇÃO ============
PASTA_CSV = "./csv"
PASTA_RELATORIO = "./relatorio"
PASTA_IMAGENS = os.path.join(PASTA_RELATORIO, "imagens")
WORKLOAD_SELECIONADO = "union_heavy"  # escolha: "union_heavy" ou "find_heavy"
IMPLEMENTACOES = ["uf_rand", "uf_rank"]
COLUNA_TEMPO = "time_us"
# ======================================

def plot_ratio():
    os.makedirs(PASTA_IMAGENS, exist_ok=True)
    todos_df = []

    # Lê todos os CSVs e filtra pelo workload selecionado
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

    # Calcula média por implementação e tamanho
    medias = df_completo.groupby(['impl', 'num_nodes'])[COLUNA_TEMPO].mean().unstack(level=0)
    # Calcula a razão UF-Rand / UF-Rank
    medias['ratio'] = medias['uf_rand'] / medias['uf_rank']

    # Configura visual
    sns.set(style="whitegrid")
    plt.figure(figsize=(20, 12))
    plt.plot(
        medias.index,
        medias['ratio'],
        'o-', 
        color='#FF3333',  # vermelho saturado
        linewidth=2,
        markersize=6,
        label='UF-Rand / UF-Rank'
    )

    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel("Tamanho do input")
    plt.ylabel("Razão média do tempo UF-Rand / UF-Rank [log-log]")
    plt.title(f"Razão Média dos Tempos - Workload: {WORKLOAD_SELECIONADO}")
    plt.legend(loc='upper left', bbox_to_anchor=(1.02,1), fontsize=12, title="Razão", title_fontsize=14)

    plt.tight_layout()
    nome_imagem = os.path.join(PASTA_IMAGENS, f"ratio_{WORKLOAD_SELECIONADO}.png")
    plt.savefig(nome_imagem, dpi=300)
    plt.show()
    plt.close()
    print(f"Gráfico salvo em: {nome_imagem}")

if __name__ == "__main__":
    plot_ratio()
