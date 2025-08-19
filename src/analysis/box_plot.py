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

def plot_boxplots():
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
                    df_filtrado['impl'] = impl  # marca a implementação
                    todos_df.append(df_filtrado)
            except Exception as e:
                print(f"Erro ao ler '{arq}': {e}")

    if not todos_df:
        print(f"Nenhum dado encontrado para o workload {WORKLOAD_SELECIONADO}")
        return

    df_completo = pd.concat(todos_df, ignore_index=True)

    sns.set(style="whitegrid")
    
    plt.figure(figsize=(20, 12)) 
    ax = sns.boxplot(
        x='num_nodes',
        y=COLUNA_TEMPO,
        hue='impl',
        data=df_completo,
        palette=['#FF3333', '#3333FF'], 
        fliersize=4,
        linewidth=1 
    )

    ax.set_yscale('log')

    y_min = df_completo[COLUNA_TEMPO].min() * 0.8
    y_max = df_completo[COLUNA_TEMPO].max() * 1.2
    ax.set_ylim(y_min, y_max)

    ax.set_xlabel("Tamanho do input", fontsize=18)
    ax.set_ylabel("Tempo (µs) [escala log]", fontsize=18)
    ax.set_title(f"Comparação UF-Rand vs UF-Rank - Workload: {WORKLOAD_SELECIONADO}", fontsize=22)

    legend = ax.legend(title="Implementação", loc='upper left', fontsize=18, title_fontsize=20)
    for text in legend.get_texts():
        text.set_fontsize(20) 
    legend.get_title().set_fontsize(22)  

    # Mostra e salva a imagem
    plt.tight_layout()
    nome_imagem = os.path.join(PASTA_IMAGENS, f"boxplot_{WORKLOAD_SELECIONADO}.png")
    plt.savefig(nome_imagem, dpi=300)
    plt.show()
    plt.close()
    print(f"Gráfico salvo em: {nome_imagem}")

if __name__ == "__main__":
    plot_boxplots()
