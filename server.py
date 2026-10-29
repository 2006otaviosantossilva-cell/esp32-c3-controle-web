
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

estado_led = "desligado"

PAGINA = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ESP32-C3 - Controle Web</title>
<style>
body {
    background: #07111f;
    color: white;
    font-family: Arial, sans-serif;
    text-align: center;
    padding: 30px 12px;
}
.container {
    max-width: 420px;
    margin: 30px auto;
    padding: 25px;
    background: #101e32;
    border: 1px solid #168cff;
    border-radius: 20px;
}
h1 { color: #38a5ff; }
#circulo {
    width: 100px;
    height: 100px;
    margin: 25px auto;
    border-radius: 50%;
    background: #333;
}
button {
    width: 100%;
    padding: 17px;
    margin: 10px 0;
    border: 0;
    border-radius: 10px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
}
.ligar { background: #00d084; }
.desligar { background: #ff4057; color: white; }
</style>
</head>
<body>
<div class="container">
<h1>ESP32-C3</h1>
<p>CONTROLE REMOTO DO LED</p>
<div id="circulo"></div>
<h2 id="estado">LED DESLIGADO</h2>
<button class="ligar" onclick="enviar('ligar')">LIGAR LED AZUL</button>
<button class="desligar" onclick="enviar('desligar')">DESLIGAR LED AZUL</button>
<p id="mensagem"></p>
</div>
<script>
async function atualizar() {
    try {
        const r = await fetch('/api/status');
        const d = await r.json();
        const ligado = d.estado === 'ligado';
        document.getElementById('estado').textContent =
            ligado ? 'LED LIGADO' : 'LED DESLIGADO';
        document.getElementById('circulo').style.background =
            ligado ? '#168cff' : '#333';
        document.getElementById('circulo').style.boxShadow =
            ligado ? '0 0 35px #168cff' : 'none';
    } catch(e) {}
}
async function enviar(comando) {
    document.getElementById('mensagem').textContent = 'Enviando comando...';
    try {
        const r = await fetch('/api/command', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({comando})
        });
        const d = await r.json();
        document.getElementById('mensagem').textContent =
            r.ok ? 'Comando registrado!' : (d.erro || 'Erro');
        atualizar();
    } catch(e) {
        document.getElementById('mensagem').textContent = 'Erro de conexão';
    }
}
atualizar();
setInterval(atualizar, 3000);
</script>
</body>
</html>
"""

@app.route("/")
def inicio():
    return render_template_string(PAGINA)

@app.route("/api/status")
def status():
    return jsonify({"estado": estado_led})

@app.route("/api/command", methods=["POST"])
def comando():
    global estado_led
    dados = request.get_json(silent=True) or {}
    novo = dados.get("comando")
    if novo not in ("ligar", "desligar"):
        return jsonify({"erro": "Comando inválido"}), 400
    estado_led = "ligado" if novo == "ligar" else "desligado"
    return jsonify({"sucesso": True, "estado": estado_led})

@app.route("/api/device/command")
def comando_dispositivo():
    return jsonify({"estado": estado_led})

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

