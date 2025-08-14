from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

TOKEN = os.getenv("TOKEN")  # Token depuis Koyeb
PHOTO_PATH = "welcome.jpg"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if os.path.exists(PHOTO_PATH):
        with open(PHOTO_PATH, "rb") as photo_file:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=photo_file,
                caption="Bienvenue sur mon bot ! 📷\nEnvoie-moi une photo et je te renverrai le fichier."
            )
    else:
        await update.message.reply_text("❌ Photo de bienvenue introuvable.")

async def photo_to_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        photo = update.message.photo[-1]
        file = await photo.get_file()
        file_path = f"{photo.file_id}.jpg"
        await file.download_to_drive(file_path)
        with open(file_path, "rb") as f:
            await update.message.reply_document(document=f, filename="image_envoyee.jpg")
    else:
        await update.message.reply_text("❌ Ce n'est pas une photo.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, photo_to_file))
    app.run_polling()
