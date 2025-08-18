#!/usr/bin/env python3
import os
import random
import sys

# ================= CONFIGURAÇÃO =================
# Probabilidades de union/fetch pesado
probs = {
    "union_heavy": 0.8,  # 80% unites
    "find_heavy": 0.8    # 80% finds
}
# Fator de operações > número de nós
OPS_FACTOR = 10  # número de operações = OPS_FACTOR * num_nodes
# ===============================================

def generate_operation(num_nodes, is_union):
    if is_union:
        a, b = random.randint(0, num_nodes-1), random.randint(0, num_nodes-1)
        return f"{a} {b}"
    else:
        x = random.randint(0, num_nodes-1)
        return f"{x}"

if len(sys.argv) != 3:
    print(f"Uso: {sys.argv[0]} <size> <workload: union_heavy|find_heavy>")
    sys.exit(1)

size = int(sys.argv[1])
workload = sys.argv[2]

if workload not in probs:
    print(f"Workload inválido: {workload}")
    sys.exit(1)

num_nodes = size
num_ops = num_nodes * OPS_FACTOR
prob_union = probs[workload]

# Criar pasta de saída
out_dir = f"input/{workload}"
os.makedirs(out_dir, exist_ok=True)
out_file = f"{out_dir}/{size}.txt"

operations = []
for _ in range(num_ops):
    if workload == "union_heavy":
        is_union = random.random() < prob_union
    else:  # find_heavy
        is_union = random.random() >= prob_union
    operations.append(generate_operation(num_nodes, is_union))

# Salvar arquivo
with open(out_file, "w") as f:
    f.write(f"{num_nodes}\n")      # número de nós
    f.write(f"{workload}\n")       # label do workload
    for op in operations:
        f.write(f"{op}\n")
