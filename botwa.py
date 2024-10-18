from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# API key untuk OpenAI
openai.api_key = 'API_KEY_OPENAI_ANDA'

# Nama panggilan pacar yang akan memicu bot
nama_pacar = "Sayang"
bot_active = False  # Status bot, aktif atau tidak

# Fungsi untuk membalas pesan menggunakan OpenAI
def generate_response(message):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Balas pesan dari pacar saya: {message}",
        max_tokens=100
    )
    return response.choices[0].text.strip()

# Endpoint untuk menerima pesan dari Twilio
@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    global bot_active
    incoming_msg = request.values.get('Body', '').strip()

    # Twilio Messaging Response
    resp = MessagingResponse()
    msg = resp.message()

    # Mengaktifkan atau menonaktifkan bot
    if nama_pacar.lower() in incoming_msg.lower():
        bot_active = True
        msg.body(f"Halo {nama_pacar}, saya aktif sekarang!")
    elif "nonaktif" in incoming_msg.lower():
        bot_active = False
        msg.body(f"Sampai jumpa, {nama_pacar}. Saya nonaktif sekarang.")
    elif bot_active:
        # Balas menggunakan model OpenAI jika bot aktif
        reply = generate_response(incoming_msg)
        msg.body(reply)
    else:
        msg.body("Saya sedang tidak aktif sekarang. Hubungi saya nanti.")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
