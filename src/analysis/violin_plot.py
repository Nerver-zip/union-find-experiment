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
WORKLOAD_SELECIONADO = "find_heavy"  # escolha: "union_heavy" ou "find_heavy"
IMPLEMENTACOES = ["uf_rand", "uf_rank"]
COLUNA_TEMPO = "time_us"
# ======================================

def plot_violin():
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

    sns.set(style="whitegrid")
    plt.figure(figsize=(20, 12))

    ax = sns.violinplot(
        x='num_nodes',
        y=COLUNA_TEMPO,
        hue='impl',
        data=df_completo,
        palette=['#FF3333', '#3333FF'],  # vermelho e azul saturados
        split=True,  # separa as duas implementações dentro do mesmo violin
        scale='width',
        inner='quartile',
        linewidth=1.5
    )

    ax.set_yscale('log')

    # Ajusta limites do eixo Y
    y_min = df_completo[COLUNA_TEMPO].min() * 0.8
    y_max = df_completo[COLUNA_TEMPO].max() * 1.2
    ax.set_ylim(y_min, y_max)

    ax.set_xlabel("Tamanho do input")
    ax.set_ylabel("Tempo (µs) [escala log]")
    ax.set_title(f"Distribuição dos Tempos - Workload: {WORKLOAD_SELECIONADO}")

    ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=12, title="Implementação", title_fontsize=14)

    plt.tight_layout()
    nome_imagem = os.path.join(PASTA_IMAGENS, f"violin_{WORKLOAD_SELECIONADO}.png")
    plt.savefig(nome_imagem, dpi=300)
    plt.show()
    plt.close()
    print(f"Gráfico salvo em: {nome_imagem}")

if __name__ == "__main__":
    plot_violin()
