import discord
import numpy as np

with open('token.txt') as f:
    token = f.readline()

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)


import requests

pokelist = np.loadtxt("pokelist.txt", delimiter=',',dtype='str')


@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name='A Cidade dos Robôs')
    channel = discord.utils.get(guild.text_channels, name='bot-fest')
    await channel.send('O bot está online!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.lower() == '!author':
            await message.channel.send('Meu autor é o Marco Moliterno!')
            await message.channel.send('(marcompp@al.insper.edu.br)')
    elif message.content.lower() == '!source':
            await message.channel.send('Meu código-fonte está em https://github.com/Marcompp/nlp_marcompp!')

    elif message.content.lower() == '!help':
            await message.channel.send('!run nome_do_pokemon: retorna o tipo, abilidades e stats do pokemon - dados fornecidos pelo site www.pokeapi.co')

    elif message.content.lower().split(' ')[0] == '!run':
            messagee = message.content.lower().split(' ') 
            payload = '-'.join(messagee[1:])
            if payload in pokelist:
                response = requests.get('https://pokeapi.co/api/v2/pokemon/'+payload)

                res = response.json()

                print(res['types'])

                for mes in [['types','type'],['abilities','ability']]:
                    mess = str(mes[0][0]).upper() + str(mes[0][1:]) + ": "
                    for thing in res[mes[0]]:
                        mess += str(thing[mes[1]]['name']) + ";  "
                    await message.channel.send(mess) 
                mess = 'Stats: '
                for stat in res['stats']:
                     mess += str(stat['stat']['name'])+":"+str(stat['base_stat'])+";  "
                await message.channel.send(mess) 
            else:
                await message.channel.send('Entrada invalida para !run') 
 
    elif isinstance(message.channel, discord.DMChannel):
        if message.content.lower() == '!oi':
            await message.channel.send('Olá em mensagem privada!')
    else:
        if message.content.lower() == '!oi':
            await message.channel.send('Olá em um canal público!')

client.run(token)

