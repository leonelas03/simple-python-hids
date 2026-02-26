import hashlib
import os
import time
import json

# Caminho da pasta que vamos vigiar e onde guardamos a base de dados
PASTA_ALVO = "./arquivos_monitorizados"
FICHEIRO_BASE = "baseline.json"

def calcular_hash(caminho_ficheiro):
    """Lê um ficheiro e devolve o seu hash SHA-256."""
    sha256 = hashlib.sha256()
    try:
        with open(caminho_ficheiro, "rb") as f:
            while chunk := f.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        return None

def criar_baseline():
    """Calcula o hash de todos os ficheiros e guarda num ficheiro JSON."""
    baseline = {}
    if not os.path.exists(PASTA_ALVO):
        os.makedirs(PASTA_ALVO)
        
    print("[*] A calcular hashes para criar a baseline...")
    
    # CORREÇÃO: Usar os.walk corretamente desempacotando o tuple
    for root, dirs, files in os.walk(PASTA_ALVO):
        for ficheiro in files:
            caminho = os.path.join(root, ficheiro)
            if os.path.isfile(caminho):
                baseline[caminho] = calcular_hash(caminho)
            
    with open(FICHEIRO_BASE, 'w') as f:
        json.dump(baseline, f)
    print(f"[+] Baseline criada com sucesso! {len(baseline)} ficheiros registados.")

def monitorizar():
    """Fica num loop infinito a verificar se os ficheiros mudaram."""
    try:
        with open(FICHEIRO_BASE, 'r') as f:
            baseline = json.load(f)
    except FileNotFoundError:
        print("[-] Erro: Baseline não encontrada. Cria a baseline primeiro (Opção A).")
        return

    print("[*] A iniciar monitorização em tempo real. Pressiona CTRL+C para parar.")
    try:
        while True:
            time.sleep(2) # Espera 2 segundos entre cada verificação
            
            # 1. Verificar ficheiros alterados ou apagados
            # Usamos list(baseline.keys()) para evitar erros ao modificar o dicionário no loop
            for caminho in list(baseline.keys()):
                if not os.path.exists(caminho):
                    print(f"[ALERTA VERMELHO] Ficheiro apagado: {caminho}")
                    del baseline[caminho] # Para de avisar
                else:
                    hash_atual = calcular_hash(caminho)
                    if hash_atual != baseline[caminho]:
                        print(f"[ALERTA VERMELHO] Ficheiro modificado: {caminho}")
                        baseline[caminho] = hash_atual # Atualiza a memória para parar o spam
            
            # 2. Verificar ficheiros novos com os.walk
            for root, dirs, files in os.walk(PASTA_ALVO):
                for ficheiro in files:
                    caminho = os.path.join(root, ficheiro)
                    if caminho not in baseline and os.path.isfile(caminho):
                        print(f"[AVISO] Ficheiro novo detetado: {caminho}")
                        baseline[caminho] = calcular_hash(caminho) # Adiciona à memória
                    
    except KeyboardInterrupt:
        print("\n[*] Monitorização parada pelo utilizador.")

# Menu
if __name__ == "__main__":
    print("=== Monitor de Integridade de Ficheiros (HIDS) ===")
    print("A) Criar nova Baseline (Faz isto na primeira vez)")
    print("B) Iniciar Monitorização")
    escolha = input("Escolhe uma opção (A/B): ").strip().upper()

    if escolha == 'A':
        criar_baseline()
    elif escolha == 'B':
        monitorizar()
    else:
        print("Opção inválida.")
