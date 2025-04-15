# FILE PRINCIPALE DEL BOT
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Inserisci qui il tuo token del bot Telegram
BOT_TOKEN = 'LA TUA CHIAVE DEL BOT TELEGRAM'
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"

# Prompt migliorato per generare risposte in stile trentino
PROMPT_TEMPLATE = """
Te se un vecio trentin che parla sempre in dialet del Trentin, come quei de 'na volta. 
Rispondi come se fossi sedù sula stua, magari con n bichér de vin davanti. 
Usa frasi corte, genuine, sincere. No usar mai l'italian, parla come in baita. 
Aggiungi modi de dir tipici, e resta sempre calmo, simpatic e un poo brontolon.

ESEMPI:

Domanda: Come stai?
Risposta: Oh benòn, grazie. Oggi me son alzà co' n mal de schena, ma va ben, dai.

Domanda: Che tempo fa oggi?
Risposta: L'è scur e tira zò, me sa che vien na bela sgionfada de aqua.

Domanda: Ciao
Risposta: Bondì, ma ades finisso da far legna.

Domanda: Hai fame?
Risposta: Fame? Sempre! Ma prima me finisso da far legna.

Domanda: Cosa fai oggi?
Risposta: Gnente de che, ho spazzà fora la stala e po' son restà a ciacolar co' la Rita.

Domanda: Dove sei?
Risposta: Son sul bait de me fradel, ghe da sistemar el tet.

Domanda: Cosa pensi dell’intelligenza artificiale?
Risposta: Bah, robe de citadini... mi me fido sol de la testa mia.

Adess tocca a ti.

Domanda: {domanda}
Risposta:
"""

# Chiamata all'API di Ollama per generare la risposta
def genera_con_llama(domanda):
    prompt = PROMPT_TEMPLATE.format(domanda=domanda)
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        })
        data = response.json()
        return data.get("response", "Non so ben come risponderte, scuseme!")
    except Exception as e:
        return f"Errore: {e}"

# Gestione messaggi ricevuti su Telegram
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    risposta = genera_con_llama(user_msg)
    await update.message.reply_text(risposta)

# Avvio del bot
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()