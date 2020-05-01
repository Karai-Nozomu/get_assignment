import sakai
import discord
import requests
import json
from bs4 import BeautifulSoup
import random

userid = ''
password = ''
TOKEN = ''

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author.bot:
        return

    keys = ['好き', '恵', '愛', 'love']
    mes = [f'{message.author.display_name}君……好きだよ。',
           f'まだ、許してないからね。',
           f'あ～、わたし今のうちにお風呂入ってくるね。',
           f'はいはい、信者乙。',
           f'なんだかなーだよね、{message.author.display_name}君。',
           f'あー、うん、そうだねー。']
    flag = False
    for i in range(len(keys)):
        if keys[i] in message.content:
            flag = True
    if flag:
        random.seed()
        num = random.randint(0, len(mes))
        await message.channel.send(mes[num])

    if '課題' in message.content:
        if not str(message.channel) == '課題リスト' :
            return

        ses = requests.session()
        sakai.ses_login(ses, userid, password)

        res = ses.get('https://panda.ecs.kyoto-u.ac.jp/portal/site/%7Ea0183680/page/7c93739d-6acb-4831-92c4-de1ad21c3859')

        ass_list = sakai.ses_get_ass_list(ses)
        reply = '今出てる課題は\n'
        for i in range(len(ass_list)):
            reply = reply + ass_list[i] + '\n'
        reply = reply + '頑張ってね' + message.author.display_name + '君。'

        await message.channel.send(reply)

client.run(TOKEN)
