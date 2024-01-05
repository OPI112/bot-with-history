import telebot
import sqlite3

API_TOKEN = '6077941896:AAFzfMFGMhBH10y8odpC2_wPl8nIkix-mb4'

bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am HistorySavingBot.
I can save your history, /delete and /show!
""")
    
# Handle '/delete' 
@bot.message_handler(commands=['delete', 'del'])
def delete_history(message):
    
    conn = sqlite3.connect('m3u3/history_database.db')
    conn.execute('DELETE FROM history WHERE chat_id = ?',(message.chat.id,))
    conn.commit()
    conn.close()
    
    bot.reply_to(message, "Your history was deleted!")    


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    text = message.text
    chat_id = message.chat.id
    date = message.date

    conn = sqlite3.connect('m3u3/history_database.db')
    conn.execute('INSERT INTO history (text, chat_id, date) values(?, ?, ?)', (text, chat_id, date))
    conn.commit()
    conn.close()

    bot.reply_to(message, message.text)


bot.infinity_polling()
