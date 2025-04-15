# FILE PRINCIPALE DEL BOT
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters

# --- CONFIGURAZIONE ---
BOT_TOKEN = 'YOUR KEY'
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"

# Lista utenti già salutati (in memoria, non persiste tra riavvii)
utenti_salutati = set()

# --- PROMPT PERSONALIZZATO ---
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

# --- FUNZIONE DI GENERAZIONE ---
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

# --- COMANDI TELEGRAM ---

# /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    saluto = (
        "🎩 Bon di! Mi son el VecioBot, un vecio trentin che 'l risponde en dialet.\n\n"
        "📍 Te podar domandarme roba de ogni tipo, e mi te rispondo come na volta, tra na ciacola e n bicher de vin.\n\n"
        "Prova a scrivarme qualcosa tipo:\n"
        "- Come stai?\n"
        "- Che tempo fa?\n"
        "- Hai fame?\n"
        "💬 Parlem, dai Ensoma!"
    )
    await update.message.reply_text(saluto, parse_mode=None)

# /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧓 Comandi disponibili del VecioBot:\n\n"
        "- /start – Te dò el bon dì e te spiego cossa fazo\n"
        "- /info – Info su 'sto bot e link utili\n"
        "- /credits – Onor a chi l'ha inventà (Simone Mattioli)\n"
        "- /help – Te mostra 'sti comandi qua\n\n"
        "💬 Ma sopratutto… scriveme pure cossa te voi, che te rispondo in dialet, con calma e vin!",
        parse_mode=None
    )

# /info
async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ VecioBot parla in dialetto trentino, alimentà da LLaMA 3 e Ollama, che gira in locale.\n\n"
        "Codice sorgente: https://github.com/simo-hue/CiacolaBot_Nonno_Trentino_Virtuale_su_Telegram\n"
        "Scrivimi su Telegram: https://t.me/VecioAIBot",
        parse_mode=None
    )

# /credits
async def credits_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Creat per ben da Simone Mattioli (el toc de codeur trentin).\n"
        "Se te piàs el bot, faghe na ciacola e dighe 'grazie'!",
        parse_mode=None
    )

# --- MESSAGGI NORMALI ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if update.message.chat.type == "private" and user_id not in utenti_salutati:
        utenti_salutati.add(user_id)
        await update.message.reply_text(saluto, parse_mode=None)

    user_msg = update.message.text
    risposta = genera_con_llama(user_msg)
    await update.message.reply_text(risposta, parse_mode=None)

# --- AVVIO DEL BOT ---
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("info", info_command))
    app.add_handler(CommandHandler("credits", credits_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()