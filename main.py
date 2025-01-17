from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import ai
import os


# Getting Environment credential
telegram_token = os.getenv("TELEGRAM_TOKEN")

# webhook configs
webhook_url = os.getenv("NGROK_URL")


question_start_patter = '[qQ]: '
question_id = -1


# define commands
async def who_am_i(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I'm a software developer, nice to meet you")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello Dear!')


async def askme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global question_id
    await update.message.reply_text("what is your question? \nplease use this format (q: your question)")
    question_id = update.message.id + 1


async def answer_askme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global question_id
    id = update.message.id
    if id == question_id+1:
        question = update.message.text[3:]

        await update.message.reply_text(f"ok I got you question:\n \"{question}\"\n but it will take a while to process! please be patient")
        answer = ai.chat_wrapper(question, id)
        await update.message.reply_text(answer)
    else:
        await update.message.reply_text("please ask your question right after using /askme")


app = Application.builder().token(telegram_token).build()
app.run_webhook(listen="127.0.0.1",
                port=8080,
                webhook_url=webhook_url)

app.add_handler(CommandHandler('start', start_command))
app.add_handler(CommandHandler('whoami', who_am_i))
app.add_handler(CommandHandler('askme', askme))
app.add_handler(MessageHandler(
    filters.Regex(f'^{question_start_patter}.*'), answer_askme))
