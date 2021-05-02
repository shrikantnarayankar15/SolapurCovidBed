from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from get_vaccine_data import getVaccine1845
url1 = 'https://solapurcovid.herokuapp.com/'
url2 = 'https://share.streamlit.io/shrikantnarayankar15/solapurcovidbed/main/main.py'

def getData():
    data18, data45 = getVaccine1845()
    if data18.shape[0]:
        return "Above 18 vaccines are Available\nCheck Below Sites\n"
    else:
        return "Above 45 Vaccines are Available\nCheck Below Sites\n"

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    notification = """
    Notification:
    This bot will keep you inform for the COVID Vaccination Availability for Solapur
    Developed by:Shrikant
    Contact No: 8983400482
    Email:k1nnn18@gmail.com"""
    update.message.reply_text(notification)
    context.job_queue.run_repeating(callback_minute, interval=60*60,
                                    context=update.message.chat_id)

def callback_minute(context):
    chat_id=context.job.context
    text = getData()
    text = text+'\n\n'+url1+'\n\n'+url2
    context.bot.send_message(chat_id=chat_id, 
                             text=text)

if __name__ == '__main__':
    updater = Updater(TOKEN_VALUE)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start",start, pass_job_queue=True))

    updater.start_polling()

    updater.idle()