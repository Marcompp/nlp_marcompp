import discord

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

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
 
    elif isinstance(message.channel, discord.DMChannel):
        if message.content.lower() == '!oi':
            await message.channel.send('Olá em mensagem privada!')
    else:
        if message.content.lower() == '!oi':
            await message.channel.send('Olá em um canal público!')

client.run('MTA3NTA2MDI3ODcyNDY1NzI5Mg.G6nfk5.n5Cqr9eb1iB8d_w9lIIOEu8pl4nUrqDP9IDJrY')

#discord.com/api/oauth2/authorize?client_id=1075060278724657292&permissions=274877978624&scope=bot