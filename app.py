import os
import sys
import requests


ENDPOINT = os.getenv("AZURE_VISION_ENDPOINT", "https://visao-inova-rmm94630.cognitiveservices.azure.com/")
KEY = os.getenv("AZURE_VISION_KEY", "Chave_aqui")

URL_API = f"{ENDPOINT.rstrip('/')}/vision/v3.2/describe"
PARAMS = {"maxCandidates": 1, "language": "en"}


def descrever_imagem(origem: str) -> dict:
    if origem.lower().startswith(("http://", "https://")):
        headers = {"Ocp-Apim-Subscription-Key": KEY, "Content-Type": "application/json"}
        resp = requests.post(URL_API, params=PARAMS, headers=headers, json={"url": origem}, timeout=30)
    else:
        headers = {"Ocp-Apim-Subscription-Key": KEY, "Content-Type": "application/octet-stream"}
        with open(origem, "rb") as f:
            resp = requests.post(URL_API, params=PARAMS, headers=headers, data=f.read(), timeout=30)
    resp.raise_for_status()
    return resp.json()


def main():
    if len(sys.argv) < 2:
        print("<Cole aqui a URL/caminho da foto>")
        sys.exit(1)

    origem = sys.argv[1]
    print(f"Enviando imagem: {origem}\n")

    try:
        resultado = descrever_imagem(origem)
    except requests.HTTPError as e:
        print(f"Erro da API: {e.response.status_code} - {e.response.text}")
        sys.exit(1)

    legendas = resultado.get("description", {}).get("captions", [])
    tags = resultado.get("description", {}).get("tags", [])

    print("------------ DESCRIÇÃO DA IMAGEM ------------")
    if legendas:
        for c in legendas:
            print(f"{c['text']}  (confiança: {c['confidence']:.0%})")
    else:
        print("Não consegui identificar a imagem! Vamos tentar novamente?")

    if tags:
        print("\nTags:", ", ".join(tags[:10]))


if __name__ == "__main__":
    main()

