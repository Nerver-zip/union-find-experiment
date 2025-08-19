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

def plot_scatter():
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
                    df_filtrado['execucao'] = range(1, len(df_filtrado)+1)  # número da execução
                    todos_df.append(df_filtrado)
            except Exception as e:
                print(f"Erro ao ler '{arq}': {e}")

    if not todos_df:
        print(f"Nenhum dado encontrado para o workload {WORKLOAD_SELECIONADO}")
        return

    df_completo = pd.concat(todos_df, ignore_index=True)

    # Configura o estilo dos plots
    sns.set(style="whitegrid")

    plt.figure(figsize=(20, 12))
    
    # Scatter plot com cores saturadas
    cores = ['#FF0000', '#0000FF']  # vermelho e azul saturados
    for impl, cor in zip(IMPLEMENTACOES, cores):
        subset = df_completo[df_completo['impl'] == impl]
        plt.scatter(
            subset['execucao'],
            subset[COLUNA_TEMPO],
            label=impl,
            color=cor,
            s=60,       # tamanho do ponto
            alpha=0.8,  # transparência
            edgecolors='w'
        )

    plt.yscale('log')

    # Ajusta limites do eixo Y
    y_min = df_completo[COLUNA_TEMPO].min() * 0.8
    y_max = df_completo[COLUNA_TEMPO].max() * 1.2
    plt.ylim(y_min, y_max)

    plt.xlabel("Execução", fontsize=22)
    plt.ylabel("Tempo (µs) [escala log]", fontsize=22)
    plt.title(f"Dispersão de execuções UF-Rand vs UF-Rank - Workload: {WORKLOAD_SELECIONADO}", fontsize=26)

    legend = plt.legend(
        title="Implementação",
        loc='upper left',
        bbox_to_anchor=(1.01, 1),
        fontsize=14,
        title_fontsize=16
    )

    plt.tight_layout()
    plt.subplots_adjust(right=0.8)  # garante espaço para legenda

    # Salva imagem
    nome_imagem = os.path.join(PASTA_IMAGENS, f"scatter_{WORKLOAD_SELECIONADO}.png")
    plt.savefig(nome_imagem, dpi=300)
    plt.show()
    plt.close()
    print(f"Gráfico salvo em: {nome_imagem}")

if __name__ == "__main__":
    plot_scatter()
