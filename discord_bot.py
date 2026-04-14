import discord
from discord.ext import commands
import asyncio

# Настройки
TOKEN = 'YOUR_BOT_TOKEN_HERE'  # Вставь сюда токен своего бота
CHANNEL_ID = 123456789012345678  # ID канала, куда писать сообщения
USER_ID = 123456789012345678  # ID пользователя, которому звонить

# Создаем интенты (нужны для доступа к голосовым каналам)
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} подключился!')

@bot.command()
async def start(ctx):
    """Команда для запуска скрипта: !start"""
    
    # Получаем канал
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        await ctx.send("Канал не найден!")
        return
    
    # Получаем пользователя
    user = await bot.fetch_user(USER_ID)
    if not user:
        await ctx.send("Пользователь не найден!")
        return
    
    # Отправляем сообщения по одному слову с переносом строки
    messages = ["привет", "как", "дела"]
    
    for word in messages:
        await channel.send(word)
        await asyncio.sleep(0.5)  # Небольшая задержка между сообщениями
    
    await asyncio.sleep(1)  # Ждем немного перед звонком
    
    # Ищем голосовой канал пользователя
    voice_channel = None
    for guild in bot.guilds:
        for member in guild.members:
            if member.id == USER_ID:
                if member.voice and member.voice.channel:
                    voice_channel = member.voice.channel
                    break
        if voice_channel:
            break
    
    if voice_channel:
        await ctx.send(f"Подключаюсь к голосовому каналу {voice_channel.name}...")
        
        # Подключаемся к голосовому каналу
        vc = await voice_channel.connect()
        
        # Здесь можно добавить воспроизведение звука или просто оставаться в канале
        await ctx.send("Подключился к голосовому чату!")
        
        # Ждем 10 секунд и отключаемся (можно убрать или изменить)
        await asyncio.sleep(10)
        await vc.disconnect()
        
        await ctx.send("Отключился от голосового канала.")
    else:
        await ctx.send("Пользователь не находится в голосовом канале!")

# Запуск бота
bot.run(TOKEN)
