import threading
import time
import random

# Configuração de sincronização
area_decolagem = threading.Semaphore(2)  # No máximo 2 aviões na área
pista_norte = threading.Lock()            # Apenas 1 avião por vez na pista norte
pista_sul = threading.Lock()              # Apenas 1 avião por vez na pista sul

def simular_fase(nome_aviao, nome_fase, min_ms, max_ms):
    tempo = random.randint(min_ms, max_ms) / 1000.0  # Converte milissegundos para segundos
    print(f"[{nome_aviao}] Iniciou fase: {nome_fase} (Duração: {tempo:.3f}s)")
    time.sleep(tempo)

def aviao(id_aviao):
    nome = f"Avião {id_aviao}"
    
    # Define a pista aleatoriamente
    pista_escolhida = random.choice(["Norte", "Sul"])
    lock_pista = pista_norte if pista_escolhida == "Norte" else pista_sul
    
    print(f"[{nome}] Pronto para decolar pela Pista {pista_escolhida}.")
    
    # Entra na área de decolagem (limite de 2 aviões no total)
    with area_decolagem:
        print(f"[{nome}] Entrou na área de decolagem.")
        
        # 1. Manobrar
        simular_fase(nome, "Manobrar", 300, 700)
        
        # 2. Taxiar
        simular_fase(nome, "Taxiar", 500, 1000)
        
        # Para decolar, precisa de exclusividade na pista escolhida
        with lock_pista:
            print(f"[{nome}] *** Entrou na Pista {pista_escolhida} ***")
            
            # 3. Decolagem
            simular_fase(nome, "Decolagem", 600, 800)
            
            # 4. Afastamento
            simular_fase(nome, "Afastamento da área", 300, 800)
            
            print(f"[{nome}] --- Decolagem concluída com sucesso e pista liberada! ---")

# Execução do Ciclo com 12 aeronaves
if __name__ == "__main__":
    print("=== INICIANDO SIMULAÇÃO DO AEROPORTO ===")
    threads = []
    
    for i in range(1, 13):
        t = threading.Thread(target=aviao, args=(i,))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    print("=== FIM DA SIMULAÇÃO (Todos os aviões decolaram) ===")