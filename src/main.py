import telebot
import pandas as pd
import seaborn as sns
import stats

sns.set(style='whitegrid', font_scale=1.3, palette='Set2')

TOKEN = 'MY-TOKEN'
bot = telebot.TeleBot(TOKEN)
df = pd.DataFrame()


@bot.message_handler(commands=['start', 'help'])
def start(message):
    '''Ответ на запросы /start, /help'''
    msg = f'Я могу помочь тебе с выбором профессии следующим образом: ты можешь написать мне интересующую тебя вакансию, а я могу дать тебе информацию по заработной плате этой профессии!'
    bot.send_message(message.chat.id, msg, parse_mode='html')


@bot.message_handler(content_types=['text'])
def send_stats(message):
    '''Отправка статистики'''
    bot.send_message(
        message.chat.id, 'Подожди немного, пожалуйста', parse_mode='html')
    df2 = stats.DF(message, bot)
    df2.salary()


bot.polling(none_stop=True)
