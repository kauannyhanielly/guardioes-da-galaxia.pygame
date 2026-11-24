"""Gera os efeitos sonoros do jogo (arquivos .wav) usando só Python.

Rode uma vez:  python gerar_sons.py
Os arquivos são criados na pasta 'sons'.
"""
import math
import os
import random
import struct
import wave

TAXA = 22050
PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sons")


def nota(freq_inicial, freq_final, duracao, forma="seno", volume=1.0, queda=4.0):
    """Cria um tom que vai de uma frequência a outra, com volume que decai."""
    total = int(TAXA * duracao)
    amostras = []
    fase = 0.0
    for i in range(total):
        t = i / total
        freq = freq_inicial + (freq_final - freq_inicial) * t
        fase += 2 * math.pi * freq / TAXA
        if forma == "quadrada":
            valor = 1.0 if math.sin(fase) >= 0 else -1.0
            valor *= 0.5
        elif forma == "serra":
            valor = ((fase / (2 * math.pi)) % 1.0) * 2 - 1
            valor *= 0.6
        else:
            valor = math.sin(fase)
        amostras.append(valor * math.exp(-queda * t) * volume)
    return amostras


def ruido(duracao, volume=1.0, queda=5.0, suavizar=0.0):
    """Ruído (tipo 'chiado') com volume que decai. 'suavizar' deixa o som mais grave."""
    total = int(TAXA * duracao)
    amostras = []
    anterior = 0.0
    for i in range(total):
        t = i / total
        bruto = random.uniform(-1, 1)
        anterior = anterior * suavizar + bruto * (1 - suavizar)
        amostras.append(anterior * math.exp(-queda * t) * volume)
    return amostras


def somar(*sons):
    """Mistura vários sons ao mesmo tempo."""
    tamanho = max(len(s) for s in sons)
    saida = [0.0] * tamanho
    for s in sons:
        for i, v in enumerate(s):
            saida[i] += v
    return saida


def sequencia(*sons):
    """Toca um som depois do outro."""
    saida = []
    for s in sons:
        saida.extend(s)
    return saida


def salvar(nome, amostras):
    pico = max(abs(v) for v in amostras) or 1.0
    escala = 0.85 / pico
    caminho = os.path.join(PASTA, nome + ".wav")
    with wave.open(caminho, "wb") as arq:
        arq.setnchannels(1)
        arq.setsampwidth(2)
        arq.setframerate(TAXA)
        dados = b"".join(struct.pack("<h", int(v * escala * 32767)) for v in amostras)
        arq.writeframes(dados)
    print("criado:", caminho)


NOTAS = {"G3": 196.0, "C4": 261.6, "E4": 329.6, "G4": 392.0, "A3": 220.0,
         "C5": 523.3, "E5": 659.3, "G5": 784.0, "C6": 1046.5, "E6": 1318.5,
         "G6": 1568.0, "A4": 440.0, "F4": 349.2, "D4": 293.7}


def arpejo(nomes, duracao_nota, forma="quadrada", queda=3.0, ultima=None):
    partes = []
    for i, n in enumerate(nomes):
        dur = ultima if (ultima and i == len(nomes) - 1) else duracao_nota
        partes.append(nota(NOTAS[n], NOTAS[n], dur, forma, 0.8, queda))
    return sequencia(*partes)


if __name__ == "__main__":
    random.seed(7)
    os.makedirs(PASTA, exist_ok=True)

    salvar("tiro", somar(nota(1200, 250, 0.17, "quadrada", 0.7, 5),
                         nota(600, 120, 0.17, "seno", 0.5, 5)))
    salvar("tiro_inimigo", nota(450, 160, 0.22, "serra", 0.8, 4))
    salvar("vazio", somar(ruido(0.05, 0.6, 8), nota(220, 180, 0.05, "quadrada", 0.5, 8)))
    salvar("acerto", nota(700, 380, 0.09, "quadrada", 0.8, 5))
    salvar("explosao", somar(ruido(0.5, 1.0, 5, 0.7), nota(110, 40, 0.5, "seno", 1.0, 4)))
    salvar("dano", somar(nota(150, 55, 0.35, "serra", 1.0, 4), ruido(0.3, 0.5, 6, 0.5)))
    salvar("fase", arpejo(["C5", "E5", "G5", "C6"], 0.09))
    salvar("vitoria", arpejo(["C5", "E5", "G5", "C6", "E6", "G6"], 0.11, ultima=0.5))
    salvar("derrota", arpejo(["A4", "F4", "D4", "A3"], 0.22, "serra", 2.5, ultima=0.6))
