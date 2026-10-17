from discord.ext import commands
import discord

intents = discord.Intents.default()
intents.message_content = True

#$
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():

    print(f'Tu bot {bot.user} esta en linea')

@bot.command()
async def saludo(ctx):

    await ctx.send('Hola que mas manitooooo')

@bot.command()
async def save(ctx):
    if ctx.message.attachments:

        for attachment in ctx.message.attachments:
            file_name = attachment.filename

            file_url = attachment.url

            await attachment.save(f'./{file_name}')

            await ctx.send(f'Archivo {file_name} guardado correctamente')

    else:
        await ctx.send('No hay archivos adjuntos para guardar')

from model import get_class

@bot.command()
async def analyze(ctx):
    if ctx.message.attachments:

        for attachment in ctx.message.attachments:
            file_name = attachment.filename

            file_url = attachment.url

            await attachment.save(f'./{file_name}')

            class_name, confidence = get_class('keras_model.h5', 'labels.txt', file_name)

            await ctx.send(f'Archivo {file_name} analizado correctamente')

            await ctx.send(f'Clase: {class_name}, Confianza: {confidence}%')

    else:
        await ctx.send('No hay archivos adjuntos para guardar')

token = ''

bot.run(token)