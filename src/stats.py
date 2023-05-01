import telebot
import requests
import json
import pandas as pd
from time import sleep
import matplotlib.pyplot as plt
import converter


class DF:
    '''Собрание статистики'''

    def __init__(self, message, bot):
        '''Инициализация датафрейма'''
        URL = 'https://api.hh.ru/vacancies'
        params = {
            'area': 1,
            'page': 0,
            'per_page': 100
        }
        self.df = pd.DataFrame()
        self.message = message
        self.bot = bot
        name = message.text
        params['text'] = name
        req = requests.get(URL, params)
        data = json.loads(req.content.decode())
        pages = data['pages']
        for page in range(pages):
            params['page'] = page
            req = requests.get(URL, params)
            data = json.loads(req.content.decode())
            self.df = pd.concat([self.df, pd.json_normalize(
                data['items'])], ignore_index=True)
            sleep(0.5)

    def salary(self):
        '''Собрание статистики о зарплате'''
        if len(self.df) == 0:
            self.bot.send_message(self.message.chat.id,
                                  'Введи корректный запрос!', parse_mode='html')
            return
        self.df['salary'] = (self.df['salary.from'] + self.df['salary.to'])/2
        self.df['salary'] = self.df.apply(converter.convert_to_rub, axis=1)
        self.df['salary'] = self.df.apply(converter.convert_to_net, axis=1)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(self.df['salary'], bins=20)
        ax.set_xlim((0, 350000))
        plt.gca().set_yticklabels([])
        ax.set_xlabel('Заработная плата в рублях (net)')
        ax.set_title(
            f'Гистограмма заработной платы профессии: {self.message.text}')
        plt.savefig('salaries.png', bbox_inches='tight')
        photo = open('salaries.png', 'rb')
        self.bot.send_photo(self.message.chat.id, photo)
