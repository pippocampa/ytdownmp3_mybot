import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

TOKEN = "8973453717:AAFT9uk3svxCFoypKqXzLlNiE6JSJPOIbTM"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao! Inviami un link di YouTube e lo convertirò in MP3. 🎵")

async def download_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not url.startswith(("http://", "https://")):
        await update.message.reply_text("Per favore, inviami un link valido.")
        return

    messaggio_attesa = await update.message.reply_text("Sto scaricando l'audio... Attendi ⏳")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        # AGGIUNGIAMO QUESTO BLOCCO PER AGGIRARE IL BLOCCO 429
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'ios'],
            }
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            mp3_path = os.path.splitext(filename)[0] + ".mp3"

        await update.message.reply_audio(audio=open(mp3_path, 'rb'), title=info.get('title'))
        os.remove(mp3_path)
        await messaggio_attesa.delete()
    except Exception as e:
        await messaggio_attesa.edit_text(f"Errore: {e}")
        if 'mp3_path' in locals() and os.path.exists(mp3_path):
            os.remove(mp3_path)

def main():
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_audio))
    
    print("Bot avviato con successo e in ascolto!")
    application.run_polling()

if __name__ == '__main__':
    main()
