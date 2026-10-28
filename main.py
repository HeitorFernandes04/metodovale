import sys

import numpy as np
from PIL import Image, ImageDraw

from limiarizacao import histograma, suavizar, metodo_vale, segmentar


def desenhar_histograma(h, T):
    # histograma em cinza, versao suavizada em preto e o limiar em vermelho
    altura = 300
    img = Image.new("RGB", (512, altura), "white")
    d = ImageDraw.Draw(img)
    s = suavizar(h)
    maior = h.max()
    for i in range(256):
        topo = altura - int(h[i] / maior * (altura - 10))
        d.rectangle([2 * i, topo, 2 * i + 1, altura], fill=(170, 170, 170))
    pontos = [(2 * i, altura - int(s[i] / maior * (altura - 10))) for i in range(256)]
    d.line(pontos, fill="black", width=2)
    d.line([(2 * T, 0), (2 * T, altura)], fill="red", width=2)
    d.text((2 * T + 5, 5), f"T = {T}", fill="red")
    return img


def main():
    if len(sys.argv) != 2:
        print("uso: python3 main.py imagem.png")
        return

    f = np.array(Image.open(sys.argv[1]).convert("L"))
    h = histograma(f)
    T = metodo_vale(h)

    if T is None:
        print("o histograma nao tem vale, a imagem nao e bimodal")
        return

    print(f"limiar encontrado pelo metodo do vale: T = {T}")
    segmentada = Image.fromarray(segmentar(f, T) * 255)
    grafico = desenhar_histograma(h, T)

    Image.fromarray(f).show(title="cinza")
    grafico.show(title="histograma")
    segmentada.show(title="segmentada")

    Image.fromarray(f).save("resultado_cinza.png")
    grafico.save("resultado_histograma.png")
    segmentada.save("resultado_segmentada.png")
    print("resultados salvos: resultado_cinza.png, resultado_histograma.png, resultado_segmentada.png")


if __name__ == "__main__":
    main()
