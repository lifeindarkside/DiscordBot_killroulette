import discord
import asyncio
import random
intents = discord.Intents().all()

client = discord.Client(intents=intents)

prizes = {
    'Новогоднее украшение': 'Добавляет эмодзи в твой никнейм и выдаёт ачивку. Шанс 2%',
    'Лошара': 'Мьют на сервере и роль ЛОШАРА на время от 1 до 60 минут. Шанс 20%',
    '| сосунок': 'Добавляет "| Сосунок" в твой никней и соответствующую роль на время от 1 до 60 минут. Шанс 78%',
}

def display_help():
    result = '\nОтправь в чат !крутанутьрулетку чтобы забрать свой приз\nВот все подарки:\n'
    for prize, description in prizes.items():
        result += f'{prize}: {description}\n'
    return result

def determine_prize():
    prize_number = random.randint(1, 500)
    if prize_number > 10 and prize_number < 20:
        return { 'name': 'Новогоднее украшение', 'description': 'Добавляет эмодзи в твой никнейм и выдаёт ачивку. Шанс 2%' }
    elif prize_number > 100 and prize_number < 200:
        return { 'name': 'Лошара', 'description': 'Мьют на сервере и роль ЛОШАРА. Шанс 20%' }
    else:
        return { 'name': '| сосунок', 'description': 'Добавляет "| Сосунок" в твой никней и соответствующую роль. Шанс 78%' }

async def perform_action(prize, user, message):
    if prize['name'] == '| сосунок':
        # Add the ending "|bad user" to the user's name on the server
        role = discord.utils.get(user.guild.roles, name='ГРУППА СОСУНКОВ')
        await user.add_roles(role)
        minutes = random.randint(1, 60)
        await message.channel.send(f"{user.mention}, твой никнейм изменен на {minutes} минут.")
        await user.edit(nick=user.name + " | сосунок")
        await asyncio.sleep(minutes * 60)
        await user.edit(nick=user.name)
        await user.remove_roles(role)
        await message.channel.send(f"{user.mention}, твой никнейм восстановлен.")
    elif prize['name'] == 'Новогоднее украшение':
        # Add a Christmas tree emoji or a gift to the user's nickname
        emojis = ['🎁', '🎄']
        emoji = random.choice(emojis)
        await message.channel.send(f'{user.mention}, меняем твой ник на '+ emoji + ' ' + user.name + ' ' + emoji)
        await user.edit(nick=emoji + ' ' + user.name + ' ' + emoji)
        role = discord.utils.get(user.guild.roles, name='Новогодний везунчик')
        await user.add_roles(role)
        role1 = discord.utils.get(user.guild.roles, name='ГРУППА СОСУНКОВ')
        try:
          await user.remove_roles(role1)
        except:
          pass
        role2 = discord.utils.get(user.guild.roles, name='ЛОШАРА')
        try:
          await user.add_roles(role2)
        except:
          pass
    elif prize['name'] == 'Лошара':
        # Give the user the "ЛОШАРА" role
        role = discord.utils.get(user.guild.roles, name='ЛОШАРА')
        await user.add_roles(role)
        # Remove the "ЛОШАРА" role after a random number of minutes
        minutes = random.randint(1, 60)
        await message.channel.send(f"{user.mention}, объявлен ЛОШАРОЙ и получил мут на сервере на {minutes} минут.\nХочешь болтать - иди в голосовой канал")
        await asyncio.sleep(minutes * 60)
        await user.remove_roles(role)
    

@client.event
async def on_ready():
    print(f'Successfully logged in as {client.user}!')

@client.event
async def on_message(message):
    if message.content.startswith('!крутанутьрулетку'):
        prize = determine_prize()
        await message.channel.send('Кручу рулетку...')
        seconds = random.randint(4,8)
        await asyncio.sleep(seconds)
        await message.channel.send(f'Ты выиграл {prize["name"]} ! {prize["description"]}')
        result = await perform_action(prize, message.author, message)
    elif message.content.startswith('!рулеткахелп'):
        embed = discord.Embed(title='Хелп по боту', description=display_help())
        await message.channel.send(embed=embed)
                 
def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

token = read_token()

client.run(token)