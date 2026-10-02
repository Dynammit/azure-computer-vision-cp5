# Inova Trônica – Visão Computacional com Azure

MVP em Python que envia uma foto ao Serviço de Visão Computacional (Azure) e exibe a descrição retornada.

## 1. Criar o serviço no Azure (etapa 1)

No portal Azure → **Criar um recurso** → **Visão Computacional** (Computer Vision):

- **Grupo de Recursos:** `rg-vc-inova`
- **Região:** uma das permitidas pela Política da sua assinatura
- **Nome:** `visao-inova-rm9999` (troque 9999 pelo RM do representante)
- **Tipo de preço:** Free (F0)

Depois de criado, tire os prints:

1. **Print 1:** aba **Visão geral** do recurso.
2. **Print 2:** aba **Chaves e Ponto de Extremidade** (pode borrar a chave).

## 2. Rodar o App (etapa 2)

```bash
pip install -r requirements.txt

# Windows (PowerShell)
$env:AZURE_VISION_ENDPOINT="https://visao-inova-rm9999.cognitiveservices.azure.com"
$env:AZURE_VISION_KEY="SUA_CHAVE"

# Linux/Mac
export AZURE_VISION_ENDPOINT="https://visao-inova-rm9999.cognitiveservices.azure.com"
export AZURE_VISION_KEY="SUA_CHAVE"

python app.py https://exemplo.com/foto-de-montanhas-e-lago.jpg
python app.py minha_foto.jpg
```

**Print 3:** terminal mostrando o comando com a foto enviada e a descrição retornada (mostre também a imagem usada).

> Não suba a chave para o GitHub. O código lê a chave de variável de ambiente.

## 3. GitHub (evidência 4)

Crie um repositório público com `app.py`, `requirements.txt` e este `README.md`, e copie o link.

## 4. Montar o PDF final

1. **Folha de rosto:** nome do Grupo + nome e RM dos integrantes.
2. Print 1 – Visão geral do recurso.
3. Print 2 – Chaves e ponto de extremidade.
4. Print 3 – Execução do App (foto enviada + descrição).
5. Link do GitHub.

Suba o PDF no Portal do Aluno → Entrega de Trabalhos (apenas **um** integrante envia).
