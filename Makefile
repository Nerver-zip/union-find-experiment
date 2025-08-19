SHELL := /bin/bash
CXX = g++
CXXFLAGS = -O3 -march=native -std=c++23

SRC_DIR = src
BIN_DIR = src/bin
CSV_DIR = csv
INPUT_DIR = input
PY_GEN = src/input_generator.py

SIZES = 1000 10000 100000 1000000
N = 30
WORKLOADS = union_heavy find_heavy
PROGS = uf_rank uf_rand

# Cores
RED    = \033[0;31m
GREEN  = \033[0;32m
YELLOW = \033[1;33m
CYAN   = \033[0;36m
RESET  = \033[0m

all: $(BIN_DIR)/uf_rank $(BIN_DIR)/uf_rand

$(BIN_DIR)/uf_rank: $(SRC_DIR)/uf_rank.cpp
	@mkdir -p $(BIN_DIR)
	@echo -e "$(CYAN)Compilando uf_rank...$(RESET)"
	$(CXX) $(CXXFLAGS) $< -o $@
	@echo -e "$(GREEN)uf_rank compilado!$(RESET)"

$(BIN_DIR)/uf_rand: $(SRC_DIR)/uf_rand.cpp
	@mkdir -p $(BIN_DIR)
	@echo -e "$(CYAN)Compilando uf_rand...$(RESET)"
	$(CXX) $(CXXFLAGS) $< -o $@
	@echo -e "$(GREEN)uf_rand compilado!$(RESET)"

run: all
	@mkdir -p $(CSV_DIR) $(INPUT_DIR)
	@TOTAL=$$(( $(words $(SIZES)) * $(words $(WORKLOADS)) * $(words $(PROGS)) * $(N) )); \
	COUNT=0; \
	for REP in $$(seq 1 $(N)); do \
		echo -e "$(YELLOW)================ REPETIÇÃO $$REP =================$(RESET)"; \
		for SIZE in $(SIZES); do \
			for WL in $(WORKLOADS); do \
				echo -e "$(YELLOW)Gerando input $$SIZE ($$WL) para REP $$REP$(RESET)"; \
				python3 $(PY_GEN) $$SIZE $$WL; \
			done \
		done; \
		for SIZE in $(SIZES); do \
			for WL in $(WORKLOADS); do \
				for PROG in $(PROGS); do \
					COUNT=$$((COUNT+1)); \
					PERCENT=$$((COUNT*100/TOTAL)); \
					EXEC=$(BIN_DIR)/$$PROG; \
					CSV_FILE=$(CSV_DIR)/$${PROG}_$$WL_$$SIZE.csv; \
					echo -e "$(CYAN)[$$PERCENT%%] Executando $$PROG | tamanho $$SIZE | workload $$WL | REP $$REP$(RESET)"; \
					$$EXEC $(INPUT_DIR)/$$WL/$$SIZE.txt $$CSV_FILE; \
					echo -e "$(GREEN)[$$PERCENT%%] Concluído: $$PROG | tamanho $$SIZE | workload $$WL | REP $$REP$(RESET)"; \
				done \
			done \
		done; \
	done
	@echo -e "$(GREEN)Todos os programas executados!$(RESET)"

clean:
	@echo -e "$(RED)Limpando arquivos binários, CSV e input...$(RESET)"
	@rm -rf $(BIN_DIR)/* $(CSV_DIR)/* $(INPUT_DIR)/*
	@echo -e "$(GREEN)Limpeza concluída!$(RESET)"
