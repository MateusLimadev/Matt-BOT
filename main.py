import random
from discord.ext import commands,tasks
import discord
from discord import app_commands
import logging
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix="!",intents=discord.Intents.all(),application_id=int(os.getenv("BOT_ID")))

class SubButton(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        self.timeout=600

        botaourl = discord.ui.Button(label="Entre no Meu Servidor!", url="https://discord.gg/xUV67QvPVH")
        self.add_item(botaourl)

@bot.event
async def on_ready(): 
    print("Estou online!")

async def pause_music():
    # código para pausar a música atualmente tocando
    # exemplo: audio.pause()
    pass

@bot.command()
@commands.is_owner() 
async def sync(ctx,guild=None):
    if guild == None:
        await bot.tree.sync()
    else:
        await bot.application_command_sync(guild=discord.Object(id=int(guild)))
    await ctx.send("Sincronizado! Se você estiver enfrentando problemas comigo, relate já no meu servidor", view=SubButton())

@bot.command()
async def play(ctx, *, song: str):
    # verificar se o autor da mensagem está em um canal de voz
    if not ctx.author.voice:
        return await ctx.send('Você precisa estar em um canal de voz para usar esse comando!')

    # conectar ao canal de voz
    channel = ctx.author.voice.channel
    await channel.connect()

    # carregar o áudio e adicioná-lo à fila de reprodução
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song))
    ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
    
    await ctx.send(f"Tocando agora: {song}")


@bot.command()
async def retomar(ctx):
    # verifica se o bot está conectado a um canal de voz
    if not ctx.voice_client:
        await ctx.send("Não estou conectado a um canal de voz.")
        return
    
    # retoma a música
    ctx.voice_client.resume()
    await ctx.send("Música retomada.")

@bot.command()
async def stop(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client.is_playing():
        voice_client.stop()
        await ctx.send("Música parada.")
    else:
        await ctx.send("Não há música tocando no momento.")


@bot.command()
async def skip(ctx):
    voice_client = ctx.guild.voice_client
    if not voice_client or not voice_client.is_playing():
        return await ctx.send("Não há música tocando no momento!")
    
    voice_client.stop()
    await ctx.send("Música pulada com sucesso!")


@bot.command()
async def queue(ctx):
    # código para exibir a fila de músicas
    pass


@bot.command()
async def clear(ctx):
    # verifica se o bot está conectado a um canal de voz
    if not ctx.voice_client:
        await ctx.send("Não estou conectado a um canal de voz.")
        return
    
    # limpa a fila de reprodução
    ctx.voice_client.queue.clear()
    await ctx.send("Fila de reprodução limpa!")

@bot.command()
async def clear_all(ctx):
    # verifica se o bot tem permissão para excluir mensagens
    if not ctx.guild.me.guild_permissions.manage_messages:
        return await ctx.send("Eu não tenho permissão para excluir mensagens!")

    # exclui todas as mensagens do canal
    await ctx.channel.purge()

    # envia uma mensagem confirmando a exclusão das mensagens
    await ctx.send("Todas as mensagens foram excluídas!")


@bot.command()
async def sair(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client:
        await voice_client.disconnect()
        await ctx.send("Saí do canal de voz.")
    else:
        await ctx.send("Não estou conectado a um canal de voz.")

@bot.command()
async def pause(ctx):
    # verifica se o bot está conectado a um canal de voz
    if not ctx.voice_client:
        await ctx.send("Não estou conectado a um canal de voz.")
        return
    
    # pausa a música
    ctx.voice_client.pause()
    await ctx.send("Música pausada.")

async def main():
    async with bot:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await bot.load_extension(f'cogs.{filename[:-3]}')

    


        TOKEN = os.getenv("DISCORD_TOKEN")
        await bot.start(TOKEN)

asyncio.run(main())
