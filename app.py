from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

ALLOWED_CHAT_IDS = [
    6842175601,
    6905173567
]

def restrict_to_allowed_chats(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        if chat_id not in ALLOWED_CHAT_IDS:
            await update.message.reply_text(f"[{chat_id}] 채팅에서는 이 봇을 사용할 수 없습니다.")
            return
        return await func(update, context)
    return wrapper

@restrict_to_allowed_chats
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("안녕하세요! /roll 명령어를 사용해 주사위를 굴려보세요!")

@restrict_to_allowed_chats
async def roll_dice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = await update.message.reply_dice()
    dice_value = message.dice.value
    await update.message.reply_text(f"주사위 결과: {dice_value} 🎲")

def main() -> None:
    TOKEN = "THE_TOKEN_HERE"

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("roll", roll_dice))

    print("봇이 실행 중입니다...")
    app.run_polling()

if __name__ == "__main__":
    main()