import os, random, discord
import blockchain

from dotenv import load_dotenv
from discord.ext.commands import Bot
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option

from commands.cmd import ping, anime, uwuify
from commands.creds import daily, wallet, give, handout, take, snoop, view_score, view_luck
from commands.valorant import getValScore
from commands.overwatch import getOWScore
from commands.submit import buy_ticket, bonusSubmit, leaderboard, claimBonus, rafflelist, top_average
from commands.helper import fetchContentList
from commands.humble import humble_powa

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILD_ID = int(os.getenv('GUILD_ID'))
CHANNEL = int(os.getenv('BOT_CMD'))
CMD_DESC = fetchContentList('command.txt')

client = Bot(command_prefix='!', intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)

keywords = ['ping', 'anime', 'uwu', 'wallet', 'give', 'handout',\
            'take', 'submit_valorant', 'view_valorant', 'submit_league',\
            'view_league', 'buy_ticket', 'bonus_submit', 'leaderboard',\
            'claim_bonus', 'humble', 'raffle', 'music_box', 'add', 'join', 'leave', 'game']

"""Either imports existing blockchain or initiates with a new genesis block"""
BLOCKCHAIN = blockchain.Blockchain()

"""Start up bot status message on boot"""
@client.event
async def on_ready(): await client.change_presence(activity=discord.Game('/uwu for fortune!'))

"""Filter message based on author and occasionally 'uwuify' read message"""
@client.event
async def on_message(message):
    if message.author.name in ['Assistant', 'Professor', 'humble', 'valuwu', 'RoleBot']: return
    if message.author == client.user: return                # checks if professor
    if message.channel.id != CHANNEL: return                # checks if from bot channel
    if message.content.split(' ')[0] in keywords: return    # checks for keywords (commands)

    if random.random() < 0.12:                              # 12% chance to get uwufied
        replace_message = uwuify(message.content)
        resend_message = f'{message.author.name}: ' + replace_message
        
        if message.author.name in ['Assistant', 'Professor']: return
        
        await message.delete()
        await client.get_channel(CHANNEL).send(resend_message)

"""Non-Blockchain dependent commands"""
@slash.slash(name='ping', description=CMD_DESC[0], guild_ids=[GUILD_ID])
async def _(ctx:SlashContext): await ping(ctx)

@slash.slash(name='anime', description=CMD_DESC[4], guild_ids=[GUILD_ID])
async def _(ctx:SlashContext): await anime(ctx)

"""Blockchin dependent commands"""
@slash.slash(name='buy_ticket', description=CMD_DESC[32], guild_ids=[GUILD_ID],
    options=[create_option(name='amount', description=CMD_DESC[36], option_type=4, required=True)])
async def _(ctx:SlashContext, amount: int): 
    await buy_ticket(ctx, amount, BLOCKCHAIN)

@slash.slash(name='uwu', description=CMD_DESC[14], guild_ids=[GUILD_ID])
async def _(ctx:SlashContext): 
    await daily (ctx, client, BLOCKCHAIN)
    await humble_powa (ctx, client, BLOCKCHAIN)

@slash.slash(name='wallet', description=CMD_DESC[15], guild_ids=[GUILD_ID])
async def _(ctx:SlashContext): await wallet(ctx, BLOCKCHAIN)

@slash.slash(name='give', description=CMD_DESC[17], guild_ids=[GUILD_ID],
    options=[create_option(name='receiver', description=CMD_DESC[18], option_type=3, required=True),
             create_option(name='amount', description=CMD_DESC[19], option_type=4, required=True)])
async def _(ctx:SlashContext, receiver: str, amount: int): 
    await give(ctx, receiver, amount, client, BLOCKCHAIN)

@slash.slash(name='handout', description=CMD_DESC[21], guild_ids=[GUILD_ID],
    options=[create_option(name='receiver', description=CMD_DESC[18], option_type=3, required=True),
             create_option(name='amount', description=CMD_DESC[19], option_type=4, required=True)])
async def _(ctx:SlashContext, receiver: str, amount: int): 
    await handout(ctx, receiver, amount, client, BLOCKCHAIN)

@slash.slash(name='take', description=CMD_DESC[23], guild_ids=[GUILD_ID],
    options=[create_option(name='victim', description=CMD_DESC[18], option_type=3, required=True),
             create_option(name='amount', description=CMD_DESC[19], option_type=4, required=True)])
async def _(ctx:SlashContext, victim: str, amount: int):
    await take(ctx, victim, amount, client, BLOCKCHAIN)

@slash.slash(name='valorant', description=CMD_DESC[24], guild_ids=[GUILD_ID],
    options=[create_option(name='title', description=CMD_DESC[55], option_type=3, required=True),
             create_option(name='link', description=CMD_DESC[56], option_type=3, required=True)])
async def _(ctx:SlashContext, title: str, link: str):
    await getValScore(ctx, title, link, BLOCKCHAIN)

@slash.slash(name='overwatch', description=CMD_DESC[48], guild_ids=[GUILD_ID],
    options=[create_option(name='title', description=CMD_DESC[55], option_type=3, required=True),
             create_option(name='link', description=CMD_DESC[56], option_type=3, required=True)])
async def _(ctx:SlashContext, title: str, link: str):
    await getOWScore(ctx, title, link, BLOCKCHAIN)
    
@slash.slash(name='leaderboard', description=CMD_DESC[34], guild_ids=[GUILD_ID])
async def _(ctx:SlashContext):
    await leaderboard(ctx, BLOCKCHAIN)

@slash.slash(name='give_submit', description=CMD_DESC[35], guild_ids=[GUILD_ID],
    options=[create_option(name='reciever', description=CMD_DESC[18], option_type=3, required=True),
             create_option(name='game', description=CMD_DESC[54], option_type=3, required=True)])
async def _(ctx:SlashContext, reciever: str, game: str): 
    await bonusSubmit(ctx, game, reciever, client, BLOCKCHAIN)

@slash.slash(name='bonus', description=CMD_DESC[37], guild_ids=[GUILD_ID])
async def _(ctx:SlashCommand):
    await claimBonus(ctx, client, BLOCKCHAIN)

@slash.slash(name='raffle', description=CMD_DESC[43], guild_ids=[GUILD_ID])
async def _(ctx:SlashCommand):
    await rafflelist(ctx, BLOCKCHAIN)

@slash.slash(name='snoop', description=CMD_DESC[22], guild_ids=[GUILD_ID],
    options=[create_option(name='target', description=CMD_DESC[18], option_type=3, required=True)])
async def _(ctx:SlashCommand, target: str):
    await snoop(ctx, target, client, BLOCKCHAIN)

@slash.slash(name='average', description=CMD_DESC[45], guild_ids=[GUILD_ID])
async def _(ctx:SlashCommand):
    await top_average(ctx, BLOCKCHAIN)

@slash.slash(name='score', description=CMD_DESC[46], guild_ids=[GUILD_ID])
async def _(ctx:SlashCommand):
    await view_score(ctx, BLOCKCHAIN)

@slash.slash(name='luck', description=CMD_DESC[47], guild_ids=[GUILD_ID])
async def _(ctx:SlashCommand):
    await view_luck(ctx, BLOCKCHAIN)

client.run(TOKEN)