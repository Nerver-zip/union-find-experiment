import pandas as pd
import glob
import os
from scipy import stats
import numpy as np

# ============ CONFIGURAÇÃO ============
PASTA_CSV = "./csv"
PASTA_RELATORIO = "./relatorio"
IMPLEMENTACOES = ["uf_rank", "uf_rand"]
WORKLOADS = ["union_heavy", "find_heavy"]
COLUNA_TEMPO = "time_us"
ALPHA = 0.05  # nível de significância
# ======================================

def verificar_normalidade(data):
    stat, p = stats.shapiro(data)
    return p > ALPHA, p  # True se normal, False se não normal

def calcular_intervalo_confianca(dif_medias, std1, std2, n1, n2, alpha=0.05):
    se_diff = np.sqrt(std1**2/n1 + std2**2/n2)
    t_crit = stats.t.ppf(1 - alpha/2, df=min(n1-1, n2-1))
    return dif_medias - t_crit*se_diff, dif_medias + t_crit*se_diff

def gerar_teste_hipotese():
    os.makedirs(PASTA_RELATORIO, exist_ok=True)
    relatorio_path = os.path.join(PASTA_RELATORIO, "testes_hipotese.txt")
    
    with open(relatorio_path, "w") as f:
        f.write("=== Teste de Hipótese: UF-Rank vs UF-Rand ===\n\n")
        
        for workload in WORKLOADS:
            f.write(f"--- Workload: {workload} ---\n")
            
            # Lê todos os CSVs das duas implementações
            dfs = {}
            for impl in IMPLEMENTACOES:
                padrao_arquivo = os.path.join(PASTA_CSV, f"{impl}_*.csv")
                arquivos_csv = glob.glob(padrao_arquivo)
                todos_df = []
                for arq in arquivos_csv:
                    df = pd.read_csv(arq)
                    df_filtrado = df[df['workload_label'] == workload]
                    if not df_filtrado.empty:
                        todos_df.append(df_filtrado)
                if todos_df:
                    dfs[impl] = pd.concat(todos_df, ignore_index=True)
            
            if len(dfs) < 2:
                f.write("Dados insuficientes para este workload.\n\n")
                continue
            
            # Pega todos os tamanhos de input
            tamanhos = sorted(set(dfs[IMPLEMENTACOES[0]]['num_nodes']).intersection(
                             dfs[IMPLEMENTACOES[1]]['num_nodes']))
            
            for tamanho in tamanhos:
                data1 = dfs[IMPLEMENTACOES[0]][dfs[IMPLEMENTACOES[0]]['num_nodes']==tamanho][COLUNA_TEMPO]
                data2 = dfs[IMPLEMENTACOES[1]][dfs[IMPLEMENTACOES[1]]['num_nodes']==tamanho][COLUNA_TEMPO]
                
                normal1, p1 = verificar_normalidade(data1)
                normal2, p2 = verificar_normalidade(data2)
                
                f.write(f"Tamanho: {tamanho}\n")
                f.write(f"UF-Rank normalidade p={p1:.4f}: {'Sim' if normal1 else 'Não'}\n")
                f.write(f"UF-Rand normalidade p={p2:.4f}: {'Sim' if normal2 else 'Não'}\n")
                
                if normal1 and normal2:
                    # t-test
                    stat, p_val = stats.ttest_ind(data1, data2)
                    dif_medias = data1.mean() - data2.mean()
                    ci_low, ci_high = calcular_intervalo_confianca(dif_medias, data1.std(), data2.std(), len(data1), len(data2))
                    metodo = "t-test de duas amostras"
                    f.write(f"Teste aplicado: {metodo}\n")
                    f.write(f"Diferença média: {dif_medias:.2f}\n")
                    f.write(f"Intervalo de confiança 95%: [{ci_low:.2f}, {ci_high:.2f}]\n")
                    f.write(f"p-valor: {p_val:.4f} -> {'Significativa' if p_val < ALPHA else 'Não significativa'}\n\n")
                else:
                    # Mann-Whitney U test
                    stat, p_val = stats.mannwhitneyu(data1, data2, alternative='two-sided')
                    metodo = "Mann-Whitney U test"
                    f.write(f"Teste aplicado: {metodo}\n")
                    f.write(f"p-valor: {p_val:.2e} -> {'Significativa' if p_val < ALPHA else 'Não significativa'}\n\n")
                    
    print(f"Relatório de testes de hipótese salvo em: {relatorio_path}")

if __name__ == "__main__":
    gerar_teste_hipotese()
