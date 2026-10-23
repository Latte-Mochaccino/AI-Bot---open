from discord.ext import commands
import discord
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True

#$
bot = commands.Bot(command_prefix='$', intents=intents)

base_folder = os.path.dirname(os.path.abspath(__file__))
img_folder = os.path.join(base_folder, "images")
check_folder = os.path.join(base_folder, "checked")
model_path = os.path.join(base_folder, "keras_model.h5")
labels_path = os.path.join(base_folder, "labels.txt")

@bot.event
async def on_ready():
    if not os.path.exists(img_folder):
        os.makedirs(img_folder)

    if not os.path.exists(check_folder):
        os.makedirs(check_folder)

    print(f'Tu bot {bot.user} esta en linea')

@bot.command()
async def saludo(ctx):

    await ctx.send('Hola que mas manitooooo')

@bot.command()
async def save(ctx):
    if ctx.message.attachments:

        for attachment in ctx.message.attachments:
            file_name = os.path.basename(attachment.filename)

            base, ext = os.path.splitext(file_name)
            counter = 1
            file_url = os.path.join(img_folder, file_name)
            while os.path.exists(file_url):
                file_name = f"{base}_{counter}{ext}"
                file_url = os.path.join(img_folder, file_name)
                counter += 1

            await attachment.save(file_url)

            await ctx.send(f'Archivo {file_name} guardado correctamente')

    else:
        await ctx.send('No hay archivos adjuntos para guardar')

from model import get_class

@bot.command()
async def show(ctx):
    files = [
        os.path.join(folder, name)
        for folder in (img_folder, check_folder)
        for name in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, name))
    ]

    if len(files) == 0:
        await ctx.send('No hay archivos guardados')
    else:
        for file_path in files:
            await ctx.send(file=discord.File(file_path))

@bot.command()
async def analyze(ctx):
    if ctx.message.attachments:

        for attachment in ctx.message.attachments:
            file_name = attachment.filename

            base, ext = os.path.splitext(file_name)
            counter = 1
            file_url = os.path.join(check_folder, file_name)
            while os.path.exists(file_url):
                file_name = f"{base}_{counter}{ext}"
                file_url = os.path.join(check_folder, file_name)
                counter += 1

            await attachment.save(file_url)

            class_name, confidence = await asyncio.to_thread(
                get_class, model_path, labels_path, file_url
            )

            await ctx.send(f'Archivo {file_name} analizado correctamente')

            await ctx.send(f'Clase: {class_name}, Confianza: {confidence}%')

    else:
        await ctx.send('No hay archivos adjuntos para guardar')

token = ''

bot.run(token)