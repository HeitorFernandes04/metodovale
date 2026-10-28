import numpy as np


def histograma(f):
    # quantos pixels tem cada nivel de cinza de 0 a 255
    return np.bincount(f.ravel(), minlength=256)


def suavizar(h, janela=15):
    # media movel pra tirar os picos pequenos de ruido do histograma
    k = janela // 2
    P = np.pad(h.astype(np.float64), k, mode="edge")
    s = np.zeros(256)
    for i in range(janela):
        s = s + P[i:i + 256]
    return s / janela


def metodo_vale(h):
    s = suavizar(h)
    vales = []
    for i in range(1, 255):
        # minimo local: nao e maior que os vizinhos
        if s[i] <= s[i - 1] and s[i] <= s[i + 1]:
            # so conta como vale se tem um pico mais alto dos dois lados
            if s[:i].max() > s[i] and s[i + 1:].max() > s[i]:
                vales.append(i)
    if not vales:
        return None
    # escolhe o vale mais perto do meio da escala de cinza
    return min(vales, key=lambda i: abs(i - 128))


def segmentar(f, T):
    # acima do limiar e objeto (1), o resto e fundo (0)
    return (f > T).astype(np.uint8)