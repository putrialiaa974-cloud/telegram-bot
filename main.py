from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime, timedelta

# === CONFIG ===
BOT_TOKEN = "8537318601:AAF1avn_-keWuRNdsPYN6jjgckYda6ZK70g"
ADMIN_USERNAME = "Iriss_MA"
ACTIVE_WINDOW_MINUTES = 10
# ==============

last_active = {}

async def record_activity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user:
        return
    username = user.username or ""
    if username.lower() == ADMIN_USERNAME.lower():
        last_active[ADMIN_USERNAME] = datetime.utcnow()

async def adminon_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.utcnow()
    cut = now - timedelta(minutes=ACTIVE_WINDOW_MINUTES)
    lines = [f"🔍 Cek Admin: @{ADMIN_USERNAME}"]
    t = last_active.get(ADMIN_USERNAME)
    if t and t >= cut:
        ago = now - t
        minutes = int(ago.total_seconds() // 60)
        seconds = int(ago.total_seconds() % 60)
        if minutes == 0:
            lines.append(f"🟢 Aktif {seconds} detik lalu")
        else:
            lines.append(f"🟢 Aktif {minutes} menit {seconds} detik lalu")
    elif t:
        lines.append(f"⚪ Terakhir aktif: {t.strftime('%Y-%m-%d %H:%M:%S')} UTC")
    else:
        lines.append("⚪ Belum ada catatan aktivitas untuk admin ini")

    await update.message.reply_text("\n".join(lines))

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot aktif. Gunakan /adminon untuk cek admin aktif.")

async def imhere_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username or ""
    if username.lower() == ADMIN_USERNAME.lower():
        last_active[ADMIN_USERNAME] = datetime.utcnow()
        await update.message.reply_text("✅ Catatan aktivitas admin diperbarui.")
    else:
        await update.message.reply_text("Kamu bukan admin.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), record_activity))
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("adminon", adminon_command))
    app.add_handler(CommandHandler("imhere", imhere_command))
    print("Bot berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
