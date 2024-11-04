import streamlit as st
from PIL import Image, ImageDraw
import random
from streamlit_keypress import keypress  # Importando a biblioteca para capturar teclas

# Função do Jogo 1: Adivinhe o Número
def jogo_adivinhe_o_numero():
    st.subheader("Adivinhe o Número")
    numero_secreto = st.session_state.get("numero_secreto", random.randint(1, 100))
    tentativa = st.number_input("Digite um número entre 1 e 100", min_value=1, max_value=100)

    if st.button("Chutar"):
        if tentativa == numero_secreto:
            st.success("Parabéns! Você acertou o número.")
            st.session_state["numero_secreto"] = random.randint(1, 100)  # Reseta o jogo
        elif tentativa < numero_secreto:
            st.warning("Tente um número maior.")
        else:
            st.warning("Tente um número menor.")

# Função do Jogo 2: Pedra, Papel ou Tesoura
def jogo_pedra_papel_tesoura():
    st.subheader("Pedra, Papel ou Tesoura")
    opcoes = ["Pedra", "Papel", "Tesoura"]
    escolha_usuario = st.selectbox("Escolha uma opção:", opcoes)
    escolha_computador = random.choice(opcoes)

    if st.button("Jogar"):
        st.write(f"Computador escolheu: {escolha_computador}")
        if escolha_usuario == escolha_computador:
            st.info("Empate!")
        elif (escolha_usuario == "Pedra" and escolha_computador == "Tesoura") or \
             (escolha_usuario == "Papel" and escolha_computador == "Pedra") or \
             (escolha_usuario == "Tesoura" and escolha_computador == "Papel"):
            st.success("Você venceu!")
        else:
            st.error("Você perdeu!")

# Função do Jogo 3: Jogo da Sorte com Dados
def jogo_dados():
    st.subheader("Jogo da Sorte com Dados")
    if st.button("Rolar o dado"):
        dado_resultado = random.randint(1, 6)
        st.write(f"O resultado do dado é: {dado_resultado}")
        if dado_resultado == 6:
            st.success("Parabéns! Você tirou o número da sorte!")
        else:
            st.info("Tente novamente para tirar um 6.")

# Função do Jogo 4: Roguelike
def jogo_roguelike():
    st.subheader("Roguelike Simples")

    # Inicializar o estado do jogo
    if "player_pos" not in st.session_state:
        st.session_state["player_pos"] = [50, 50]  # Posição inicial do personagem
        st.session_state["boss_pos"] = [random.randint(0, 300), random.randint(0, 300)]
        st.session_state["player_size"] = 20
        st.session_state["player_shape"] = "quadrado"  # Pode ser "quadrado" ou "círculo"
        st.session_state["boss_capturado"] = False

    # Função para desenhar o mapa como imagem
    def desenha_mapa():
        # Cria uma imagem com fundo verde
        mapa = Image.new("RGB", (400, 400), "green")
        draw = ImageDraw.Draw(mapa)

        # Desenha o personagem
        px, py = st.session_state["player_pos"]
        tamanho = st.session_state["player_size"]
        if st.session_state["player_shape"] == "quadrado":
            draw.rectangle(
                [px, py, px + tamanho, py + tamanho],
                fill="blue"
            )
        elif st.session_state["player_shape"] == "círculo":
            draw.ellipse(
                [px, py, px + tamanho, py + tamanho],
                fill="blue"
            )

        # Desenha o boss
        bx, by = st.session_state["boss_pos"]
        draw.rectangle(
            [bx, by, bx + 20, by + 20],
            fill="red"
        )

        return mapa

    # Função para mover o personagem
    def mover_personagem(dx, dy):
        st.session_state["player_pos"][0] += dx
        st.session_state["player_pos"][1] += dy
        mover_boss()
        checar_colisao()

    # Função para mover o boss aleatoriamente
    def mover_boss():
        bx, by = st.session_state["boss_pos"]
        movimento_boss = random.choice([(10, 0), (-10, 0), (0, 10), (0, -10)])  # Movimento aleatório
        bx = min(max(bx + movimento_boss[0], 0), 380)  # Mantém o boss dentro dos limites do mapa
        by = min(max(by + movimento_boss[1], 0), 380)
        st.session_state["boss_pos"] = [bx, by]

    # Função para checar colisão com o boss
    def checar_colisao():
        px, py = st.session_state["player_pos"]
        bx, by = st.session_state["boss_pos"]
        tamanho = st.session_state["player_size"]

        # Verifica se há colisão
        if (bx < px + tamanho and px < bx + 20) and \
           (by < py + tamanho and py < by + 20):
            st.session_state["boss_capturado"] = True
            escolher_power_up()

    # Função para escolher o power-up após derrotar o boss
    def escolher_power_up():
        if st.session_state["boss_capturado"]:
            escolha = st.radio("Escolha um poder:", ["Crescer", "Mudar de forma"], key="power_up_choice")
            if st.button("Confirmar escolha"):
                if escolha == "Crescer":
                    st.session_state["player_size"] += 15  # Aumenta significativamente o tamanho do personagem
                elif escolha == "Mudar de forma":
                    nova_forma = "círculo" if st.session_state["player_shape"] == "quadrado" else "quadrado"
                    st.session_state["player_shape"] = nova_forma
                # Coloca o boss em nova posição e reseta o estado de captura
                st.session_state["boss_pos"] = [random.randint(0, 300), random.randint(0, 300)]
                st.session_state["boss_capturado"] = False
                st.experimental_rerun()  # Atualiza o mapa com a nova escolha

    # Captura de teclas
    tecla = keypress()
    if tecla in ['w', 'W', 'ArrowUp']:
        mover_personagem(0, -10)
    elif tecla in ['s', 'S', 'ArrowDown']:
        mover_personagem(0, 10)
    elif tecla in ['a', 'A', 'ArrowLeft']:
        mover_personagem(-10, 0)
    elif tecla in ['d', 'D', 'ArrowRight']:
        mover_personagem(10, 0)

    # Desenha o jogo
    mapa = desenha_mapa()
    st.image(mapa, caption="Mapa do Jogo")

# Estrutura Principal com Tabs
st.title("App de Jogos em Streamlit")
abas = st.tabs(["Adivinhe o Número", "Pedra, Papel ou Tesoura", "Jogo da Sorte com Dados", "Roguelike"])

with abas[0]:
    jogo_adivinhe_o_numero()

with abas[1]:
    jogo_pedra_papel_tesoura()

with abas[2]:
    jogo_dados()

with abas[3]:
    jogo_roguelike()
