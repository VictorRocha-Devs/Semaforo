import threading
import time
import random

# Locks para garantir exclusividade dos itens
lock_tocha = threading.Lock()
lock_pedra = threading.Lock()
lock_portas = threading.Lock()

# Recursos globais
tocha_disponivel = True
pedra_disponivel = True
cavaleiro_com_tocha = None

# Preparação das portas (1 saída, 3 monstros)
portas_disponiveis = ["SAÍDA", "MONSTRO", "MONSTRO", "MONSTRO"]
random.shuffle(portas_disponiveis) # Embaralha as portas secretamente

posicoes_finais = []

def cavaleiro(nome):
    global tocha_disponivel, pedra_disponivel, cavaleiro_com_tocha
    
    distancia = 0
    corredor_total = 2000 # 2 km em metros
    passo_tempo = 0.050   # 50 ms
    
    tem_tocha = False
    tem_pedra = False
    
    print(f"[{nome}] Iniciou a caminhada no corredor escuro!")
    
    while distancia < corredor_total:
        # Velocidade base: de 2 a 4 metros
        velocidade = random.randint(2, 4)
        
        # Bônus de velocidade
        if tem_tocha:
            velocidade += 2
        if tem_pedra:
            velocidade += 2
            
        distancia += velocidade
        time.sleep(passo_tempo)
        
        # Evento: Tocha aos 500m
        if distancia >= 500 and tocha_disponivel:
            with lock_tocha:
                if tocha_disponivel: # Double-check locking
                    tocha_disponivel = False
                    tem_tocha = True
                    cavaleiro_com_tocha = nome
                    print(f"[{nome}] [!] PEGOU A TOCHA aos {distancia}m! Velocidade aumentada.")
                    
        # Evento: Pedra Brilhante aos 1500m
        if distancia >= 1500 and pedra_disponivel:
            with lock_pedra:
                # Só pode pegar se estiver disponível E o cavaleiro não tiver a tocha
                if pedra_disponivel and cavaleiro_com_tocha != nome:
                    pedra_disponivel = False
                    tem_pedra = True
                    print(f"[{nome}] [!] PEGOU A PEDRA BRILHANTE aos {distancia}m! Velocidade aumentada.")

    print(f"[{nome}] Chegou ao final dos 2 km!")
    
    # Fase das Portas (um por vez escolhe)
    with lock_portas:
        porta_escolhida = portas_disponiveis.pop(0) # Pega a próxima porta da lista embaralhada
        resultado = "SOBREVIVEU!" if porta_escolhida == "SAÍDA" else "FOI DEVORADO POR MONSTROS!"
        posicoes_finais.append((nome, resultado))
        print(f"[{nome}] Escolheu uma porta... Resultado: {resultado}")

if __name__ == "__main__":
    print("=== INICIANDO A JORNADA DOS CAVALEIROS ===")
    
    nomes_cavaleiros = ["Cavaleiro Artur", "Cavaleiro Lancelot", "Cavaleiro Galahad", "Cavaleiro Gawain"]
    threads = []
    
    for nome in nomes_cavaleiros:
        t = threading.Thread(target=cavaleiro, args=(nome,))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    print("\n=== RESUMO DO DESTINO DOS CAVALEIROS ===")
    for i, (nome, res) in enumerate(posicoes_finais, 1):
        print(f"{i}º Lugar: {nome} -> {res}")