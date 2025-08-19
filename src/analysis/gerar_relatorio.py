import pandas as pd
import glob
import os

# ============ CONFIGURAÇÃO ============
PASTA_CSV = "./csv"
PASTA_RELATORIO = "./relatorio"

IMPLEMENTACOES = ["uf_rank", "uf_rand"]
WORKLOADS = ["union_heavy", "find_heavy"]
COLUNA_TEMPO = "time_us"  # coluna com tempo de execução
# ======================================

def gerar_relatorios_union_find():
    os.makedirs(PASTA_RELATORIO, exist_ok=True)

    for impl in IMPLEMENTACOES:
        for workload in WORKLOADS:
            padrao_arquivo = os.path.join(PASTA_CSV, f"{impl}_*.csv")
            arquivos_csv = glob.glob(padrao_arquivo)

            if not arquivos_csv:
                print(f"Nenhum arquivo encontrado para {impl}")
                continue

            todos_df = []
            for arquivo in arquivos_csv:
                try:
                    df = pd.read_csv(arquivo)
                    # Filtra apenas as linhas do workload atual
                    df_filtrado = df[df['workload_label'] == workload]
                    if not df_filtrado.empty:
                        todos_df.append(df_filtrado)
                except Exception as e:
                    print(f"Erro ao ler '{arquivo}': {e}")

            if not todos_df:
                print(f"Nenhum dado válido encontrado para {impl} + {workload}")
                continue

            # Concatena todos os dados
            df_completo = pd.concat(todos_df, ignore_index=True)

            # Agrupa por tamanho do input e calcula estatísticas
            estatisticas = df_completo.groupby("num_nodes")[COLUNA_TEMPO].agg([
                ("media", "mean"),
                ("mediana", "median"),
                ("desvio_padrao", "std"),
                ("minimo", "min"),
                ("maximo", "max"),
                ("amostras", "count")
            ]).reset_index()

            estatisticas["coeficiente_variacao"] = estatisticas["desvio_padrao"] / estatisticas["media"]

            # Nome do arquivo de saída claro
            nome_saida = os.path.join(
                PASTA_RELATORIO,
                f"estatisticas_{impl}_{workload}.csv"
            )

            estatisticas.to_csv(nome_saida, index=False, sep=';', float_format="%.2f")
            print(f"Relatório salvo em: {nome_saida}")

if __name__ == "__main__":
    gerar_relatorios_union_find()
