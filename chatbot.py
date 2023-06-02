import discord
import numpy as np

import requests
from bs4 import BeautifulSoup
import sqlite3

#import functions
import validators

import nltk

from nltk.corpus import wordnet
nltk.download('wordnet')
nltk.download('omw-1.4')
import os
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser

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

    elif message.content.lower().split(' ')[0] == '!crawl':
        messagee = message.content.lower().split(' ') 
        url = []
        url.append( '-'.join(messagee[1:]) )
        #chat gpt
        if validators.url(url[0]):
            step = 0
             # Send a GET request to the URL
            await message.channel.send('Crawling iniciado') 

            while (step < 15) and len(url) > 0 and validators.url(url[0]):

                currurl = url.pop(0)
                
                response = requests.get(currurl)

                # Parse the HTML content using BeautifulSoup
                soup = BeautifulSoup(response.content, "html.parser")

                url += list(soup.find_all("a"))

                # Extract the page content
                page_content = str(soup)

                await message.channel.send('Crawling em progresso') 

                # Connect to a SQLite database
                conn = sqlite3.connect("crawl.db")

                # Create a table to store the page content
                conn.execute("CREATE TABLE IF NOT EXISTS crawl (id INTEGER PRIMARY KEY, url TEXT, content TEXT)")

                # Insert the page content into the database
                conn.execute("INSERT INTO crawl (url, content) VALUES (?, ?)", (currurl, str(page_content)))
                conn.commit()

                # Close the database connection
                conn.close()
                step +=1
                if len(url) > 0:
                    url[0] = url[0].get('href')

            
            
            # Create or open the index directory
            index_dir = "index"
            if not os.path.exists(index_dir):
                os.mkdir(index_dir)
            ix = create_in(index_dir, Schema(url=ID(stored=True), content=TEXT))

            # Open the index writer
            writer = ix.writer()

            # Open the database connection
            conn = sqlite3.connect("crawl.db")

            # Retrieve the pages from the database
            cursor = conn.execute("SELECT url, content FROM crawl")

            # Index each page
            for row in cursor:
                await message.channel.send('Aplicando index reversa') 
                urll = row[0]
                content = row[1]
                writer.add_document(url=urll, content=content)

            # Commit the changes to the index
            writer.commit()

            # Close the index writer
            #writer.close()

            # Close the database connection
            conn.close()

            await message.channel.send('Crawling finalisado') 
        else:
            await message.channel.send('Entrada invalida para !crawl') 

    elif message.content.lower().split(' ')[0] == '!search':
        messagee = message.content.lower().split(' ') 
        payload = ' '.join(messagee[1:])


        # Connect to the database
        conn = sqlite3.connect('crawl.db')

        # Create a cursor object
        c = conn.cursor()

        # Search for records containing the word 'example'
        c.execute("SELECT * FROM crawl WHERE content LIKE ?", ('%'+payload+'%',))

        # Fetch the results
        results = c.fetchall()

        #print(results[1][1])
        # Close the database connection
        conn.close()
        await message.channel.send(str(results[1][1]) )


    elif message.content.lower().split(' ')[0] == '!wn_search':
        messagee = message.content.lower().split(' ') 
        if len(messagee) == 2:
            payload = messagee[1]


            # Connect to the database
            conn = sqlite3.connect('crawl.db')

            # Create a cursor object
            c = conn.cursor()

            # Search for words in the database
            synsets = wordnet.synsets(payload)
            for synset in synsets:
                lemma = synset.lemmas()[0].name()
                c.execute("SELECT * FROM crawl WHERE content LIKE ?", ('%'+lemma+'%',))
                results = c.fetchall()
                #print(results)
                await message.channel.send(str(results[1][1]) )

            # Close the database connection
            conn.close()
        else:
            await message.channel.send('Entrada invalida para !run') 


    
 
    elif isinstance(message.channel, discord.DMChannel):
        if message.content.lower() == '!oi':
            await message.channel.send('Olá em mensagem privada!')
    else:
        if message.content.lower() == '!oi':
            await message.channel.send('Olá em um canal público!')

client.run(token)

