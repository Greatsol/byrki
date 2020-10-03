# -*- coding: utf-8 -*-

import requests
import telebot

token ='888945414:AAFzG8NcwoO_OyWrzS_UOU1kvhXN2SrL1HE'
bot = telebot.TeleBot(token)

def write_id(chat_id):

    ids = open('~/byrki/ids.txt', 'a')
    ids.write(str(chat_id) + '\n')
    bot.send_message(687185782, 'New id: {}'.format(chat_id))


def serch_id(chat_id):

    ids = open('~/byrki/ids.txt', 'r')
    text = ids.read()
    if str(chat_id) in text:
        return False
    else:
        return True

def point(amount):
    point = amount.find(',')
    amount = list(amount)
    if point != -1:
        amount[point] = '.'
    return ''.join(amount)


def send_all_users(gg):

    ids = open('~/byrki/ids.txt', 'r')
    text = ids.read()
    i = 0
    j = 9
    l = len(text)
    for e in text:
        if i >= l:
            break
        user_id = text[i:j]
        try:
            bot.send_message(int(user_id), gg)
        except:
            print('chat {} do not found'.format(user_id))
        i += 10
        j += 10


def get_price():

    ids = {'usd':'145', 'eur':'292', 'rub':'298', 'uah':'290', 'plz':'293', 'czk':'305', 'bgn':'191'}
    i = ['145', '292', '298', '290', '293', '305', '191']
    price = []
    for k in i:
        link = 'http://www.nbrb.by/API/ExRates/Rates/' + k
        r = requests.get(link)
        r = r.json()
        r = r['Cur_OfficialRate']
        if k in ['298', '290', '305']:
            price.append(float(r)/100)
        elif k == '293':
            price.append(float(r)/10)
        else:
            price.append(float(r))
    print(price)
    return price


def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"


def byn_to(amount, price):
    output = []
    if int(amount) == int:
        output.append(amount)
    else:
        output.append((toFixed(amount, 2)))
    for element in price:
        output.append(toFixed(float(amount) / float(element), 2))
    return output


def conversion(amount, status, price):
    amount = float(amount)
    if status == 'byn':
        return byn_to(amount, price)
    else:
        inbyn = amount * price[int(status)]
        return byn_to(inbyn, price)

def points_counter(amount):
    k = 0
    for element in amount:
        if element in ['.', ',']:
            k += 1
    return k


@bot.message_handler(commands = ['start', 'help'])
def main(message):
    bot.send_message(message.chat.id, '''Для использавния бота напишите сумму и валюту.\nПримеры:\n5 usd/доллар/бакс\n5 eur/евро\n5 rub/руб/р\n5 без пробела/byn\n5 uah/a/гривна/грн\n5 plz/pln/злот/злт\n5 czk/крон/cz\n5 bgn/bg/лев''')
    if serch_id(message.chat.id):
        write_id(message.chat.id)


@bot.message_handler(content_types = ['text'])
def main(message):
    msg = message.text
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', ',']
    usd = ['usd', 'бакс', 'доллар', '$']
    eur = ['€', 'евро', 'eur', 'gh[hhg']
    byn = ['бел руб', 'byn', 'rr[rr', 'ghh[hg']
    rub = ['р', 'руб', 'rub', 'Р']
    uah = ['uah', 'гривна', 'грн', 'ua']
    plz = ['plz', 'злт', 'злот', 'pl[n']
    czk = ['czk', 'cz', 'крон', 'g[fhdfhg']
    bgn = ['bgn', 'лев', 'bg', 'prp[s']
    amount = ''
    res = False

    for element in msg:
        if element in numbers:
            amount += element

    for i in range(0, 3):
        if (msg.find(usd[i]) != -1) and (amount != ''):
            res = '0'
        if (msg.find(rub[i]) != -1) and (amount != ''):
            res = '2'
        if (msg.find(byn[i]) != -1) and (amount != ''):
            res = 'byn'
        if (msg.find(eur[i]) != -1) and (amount != ''):
            res = '1'
        if (msg.find(uah[i]) != -1) and (amount != ''):
            res = '3'
        if (msg.find(plz[i]) != -1) and (amount != ''):
            res = '4'
        if (msg.find(czk[i]) != -1) and (amount != ''):
            res = '5'
        if (msg.find(bgn[i]) != -1) and (amount != ''):
            res = '6'
        if (' ' not in msg) and (amount != ''):
            res = 'byn'

    price = get_price()
    if res:
        if points_counter(amount) > 1:
            bot.send_message(message.chat.id, 'Ошибка ввода.')
        else:
            end = conversion(point(amount), res, price)
            bot.send_message(687185782, 'text = "{}"\tres = {}\tamount = {}\tchat_id = {}'.format(msg, res, amount, message.chat.id))
            msg = '\U0001F1E7\U0001F1FE {}\n\U0001F1FA\U0001F1F8 {}\n\U0001F1EA\U0001F1FA {}\n\U0001F1F7\U0001F1FA {}\n\U0001F1FA\U0001F1E6 {}\n\U0001F1F5\U0001F1F1 {}\n\U0001F1E8\U0001F1FF {}\n\U0001F1E7\U0001F1EC {}'.format(*end)
            bot.send_message(message.chat.id, msg)





if __name__ == '__main__':
    print('start')
    bot.polling(none_stop=True)
'''687185782
378566095
521658494
576255102'''
