import discord

with open('token.txt') as f:
    token = f.readline()

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)


import requests



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
            payload = messagee[1]
            #if payload not in ()
            response = requests.get('https://pokeapi.co/api/v2/pokemon/'+payload)

            res = response.json()

            print(res['types'])

            for mes in ['types','abilities','stats']:
                await message.channel.send(mes + ":  " +str(res[mes])) 
 
    elif isinstance(message.channel, discord.DMChannel):
        if message.content.lower() == '!oi':
            await message.channel.send('Olá em mensagem privada!')
    else:
        if message.content.lower() == '!oi':
            await message.channel.send('Olá em um canal público!')

client.run(token)

