# Union-Find Experiment

Este repositório contém experimentos comparando duas variações do algoritmo **Union-Find**:  
- Union by Rank  
- Randomized Linking  

O objetivo é avaliar o desempenho empírico das duas abordagens em diferentes cargas de trabalho e tamanhos de entrada.

---

## Estrutura do Repositório

```
├── csv/          # Resultados brutos em CSV
├── input/        # Instâncias geradas para os experimentos
├── relatorio/    # Relatório com análise e visualizações
├── src/          # Implementações C++ e gerador de input
├── Makefile      # Automação de compilação e execução
├── requirements.txt
└── README.md
```

---

## Reprodutibilidade

Todas as implementações (Union-Find, gerador de entradas e scripts de execução), assim como os resultados brutos em CSV, estão disponíveis neste repositório.  
Isso permite **reproduzir todos os experimentos** e **validar as análises** de forma independente.

---

## Como Rodar

### 1. Instalar dependências
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 2. Compilar os programas
```bash
make
```

### 3. Executar os experimentos
```bash
make run
```

Os resultados serão salvos na pasta `csv/`.

### 4. Limpar artefatos
```bash
make clean
```

---

## Relatório

A análise detalhada dos resultados está disponível em:  
[\`relatorio/\`](./relatorio)

---
