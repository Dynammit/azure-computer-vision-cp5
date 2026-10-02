import base64
import os

import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

ENDPOINT = os.getenv("AZURE_VISION_ENDPOINT", "https://SEU-RECURSO.cognitiveservices.azure.com/")
KEY = os.getenv("AZURE_VISION_KEY", "Chave_aqui")
URL_API = f"{ENDPOINT.rstrip('/')}/vision/v3.2/describe"

PAGE = """
<!doctype html>
<html lang="pt-br">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Inova Trônica - Visão Computacional</title>
<style>
  :root { --azul:#0b3d91; --azul2:#1c6ed5; --fundo:#eef4fc; --card:#fff; --texto:#1b2a41; }
  * { box-sizing: border-box; }
  body { margin:0; font-family: "Segoe UI", Arial, sans-serif; background:var(--fundo); color:var(--texto); }
  header { background:linear-gradient(135deg,var(--azul),var(--azul2)); color:#fff; padding:28px 20px; text-align:center; }
  header h1 { margin:0 0 6px; font-size:1.7rem; }
  header p { margin:0; opacity:.9; }
  main { max-width:900px; margin:24px auto; padding:0 16px; display:grid; gap:20px; }
  .card { background:var(--card); border-radius:14px; padding:22px; box-shadow:0 2px 10px rgba(11,61,145,.1); }
  label { display:block; font-weight:600; margin:14px 0 6px; }
  input[type=url], input[type=file], select { width:100%; padding:10px; border:1px solid #c5d3ea; border-radius:8px; font-size:1rem; background:#fff; }
  button { margin-top:18px; width:100%; padding:13px; border:0; border-radius:10px; background:var(--azul2); color:#fff; font-size:1.05rem; font-weight:600; cursor:pointer; }
  button:hover { background:var(--azul); }
  .ou { text-align:center; color:#6a7a96; margin:10px 0 0; font-size:.9rem; }
  .resultado { display:grid; grid-template-columns:1fr 1fr; gap:20px; align-items:start; }
  @media (max-width:700px) { .resultado { grid-template-columns:1fr; } }
  .resultado img { width:100%; border-radius:10px; }
  .legenda { font-size:1.35rem; font-weight:600; color:var(--azul); margin:0 0 8px; }
  .conf { color:#3d5a8a; margin:0 0 14px; }
  .tags span { display:inline-block; background:#e0ecff; color:var(--azul); padding:4px 10px; border-radius:20px; margin:0 6px 6px 0; font-size:.9rem; }
  .erro { background:#fdecec; color:#9b1c1c; border-radius:10px; padding:14px; }
  footer { text-align:center; color:#6a7a96; font-size:.85rem; padding:10px 0 30px; }
</style>
</head>
<body>
<header>
  <h1>Descrição de Imagens com IA</h1>
  <p>Serviço de Visão Computacional do Azure &middot; MVP Inova Trônica</p>
</header>
<main>
  <form class="card" method="post" enctype="multipart/form-data">
    <label for="arquivo">Enviar uma foto do computador</label>
    <input type="file" id="arquivo" name="arquivo" accept="image/*">
    <p class="ou">ou</p>
    <label for="url">Colar o link (URL) de uma imagem</label>
    <input type="url" id="url" name="url" placeholder="https://exemplo.com/foto.jpg" value="{{ url or '' }}">
    <label for="idioma">Idioma da descrição</label>
    <select id="idioma" name="idioma">
      <option value="pt" {{ 'selected' if idioma == 'pt' else '' }}>Português</option>
      <option value="en" {{ 'selected' if idioma == 'en' else '' }}>English</option>
      <option value="es" {{ 'selected' if idioma == 'es' else '' }}>Español</option>
    </select>
    <button type="submit">Descrever imagem</button>
  </form>

  {% if erro %}
  <div class="erro"><strong>Não foi possível analisar:</strong> {{ erro }}</div>
  {% endif %}

  {% if legendas %}
  <section class="card resultado">
    <div><img src="{{ preview }}" alt="Imagem analisada"></div>
    <div>
      {% for c in legendas %}
        <p class="legenda">{{ c.text }}</p>
        <p class="conf">Confiança: {{ (c.confidence * 100) | round | int }}%</p>
      {% endfor %}
      {% if tags %}
        <div class="tags">
          {% for t in tags %}<span>{{ t }}</span>{% endfor %}
        </div>
      {% endif %}
    </div>
  </section>
  {% endif %}
</main>
<footer>Desenvolvido com Azure AI Vision</footer>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    ctx = dict(url="", idioma="pt", erro=None, legendas=None, tags=None, preview=None)
    if request.method == "POST":
        ctx["url"] = request.form.get("url", "").strip()
        ctx["idioma"] = request.form.get("idioma", "pt")
        arquivo = request.files.get("arquivo")
        params = {"maxCandidates": 1, "language": ctx["idioma"]}

        try:
            if arquivo and arquivo.filename:
                dados = arquivo.read()
                headers = {"Ocp-Apim-Subscription-Key": KEY, "Content-Type": "application/octet-stream"}
                resp = requests.post(URL_API, params=params, headers=headers, data=dados, timeout=30)
                mime = arquivo.mimetype or "image/jpeg"
                ctx["preview"] = f"data:{mime};base64," + base64.b64encode(dados).decode()
            elif ctx["url"]:
                headers = {"Ocp-Apim-Subscription-Key": KEY, "Content-Type": "application/json"}
                resp = requests.post(URL_API, params=params, headers=headers, json={"url": ctx["url"]}, timeout=30)
                ctx["preview"] = ctx["url"]
            else:
                ctx["erro"] = "Envie uma foto ou cole o link de uma imagem."
                return render_template_string(PAGE, **ctx)

            resp.raise_for_status()
            desc = resp.json().get("description", {})
            ctx["legendas"] = desc.get("captions", [])
            ctx["tags"] = desc.get("tags", [])[:10]
            if not ctx["legendas"]:
                ctx["erro"] = "Nenhuma descrição foi retornada para esta imagem."
        except requests.HTTPError as e:
            ctx["erro"] = f"Erro da API ({e.response.status_code}). Confira a chave e o endpoint."
        except requests.RequestException as e:
            ctx["erro"] = f"Falha de conexão: {e}"

    return render_template_string(PAGE, **ctx)


if __name__ == "__main__":
    app.run(debug=True)
