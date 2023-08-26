import sys
import discord
from discord.ext import commands
import requests

TOKEN = 'YOUR_DISCORD_BOT_TOKEN'
YOUR_CHANNEL_ID = 1126012280488869888  # Discord channel ID


# Check if the parameter is passed or not
if len(sys.argv) > 1:
    # Take the first parameter
    TOKEN = sys.argv[1]
else:
    print("Không có tham số được truyền vào.")

print("BOT TOKEN là:", TOKEN)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

def get_bullshark_info(address):
    try:
        url = f'https://quests.mystenlabs.com/api/trpc/user?batch=1&input={{"0":{{"address":"{address}","questId":2}}}}'
        response = requests.get(url)
        data = response.json()
        return data
    except Exception as e:
        return "Không thể lấy dữ liệu từ MystenLab"

@bot.event
async def on_ready():
    print(f'Bot đã đăng nhập với tên {bot.user}')

@bot.command(name='bullshark')
async def bullshark_info(ctx, address):
    if len(address) != 66 or not address.startswith('0x'):
        await ctx.send('Địa chỉ SUI không hợp lệ.')
        return

    try:
        info = get_bullshark_info(address)
        result = info[0]['result']['data']
        score = result['score']
        bot_status = result['bot']
        rank = result['rank']
        reward = result['reward']
        metadata = result['metadata']
        SUI_TVL = metadata['SUI_TVL']
        NAVI_VALUE = metadata['NAVI_VALUE']
        CETUS_VALUE = metadata['CETUS_VALUE']
        KRIYA_VALUE = metadata['KRIYA_VALUE']
        TYPUS_VALUE = metadata['TYPUS_VALUE']
        TURBOS_VALUE = metadata['TURBOS_VALUE']
        SCALLOP_VALUE = metadata['SCALLOP_VALUE']
        NON_SUI_TVL =  metadata['NON_SUI_TVL_IN_USD']
        Apps_used = metadata['appsUsed']
        Apps_used_num = len(Apps_used)
        response_message = f"### SCORE: **{score}**\n### BOT FLAG: **{bot_status}**\n### RANK: **{rank}**\n### REWARD: **{reward}**\n"
        response_message += f"> SUI TVL: **{SUI_TVL}** SUI\n"
        response_message += f"> NON SUI TVL: **{NON_SUI_TVL}** USD\n"
        response_message += f"> NAVI Points: {NAVI_VALUE}\n"
        response_message += f"> CETUS Points: {CETUS_VALUE}\n"
        response_message += f"> KRIYA Points: {KRIYA_VALUE}\n"
        response_message += f"> TYPUS Points: {TYPUS_VALUE}\n"
        response_message += f"> TURBOS Points: {TURBOS_VALUE}\n"
        response_message += f"> SCALLOP Points: {SCALLOP_VALUE}\n"
        response_message += f"### APPs USED: {Apps_used_num}/6\n"
        await ctx.message.reply(response_message)
    except Exception as e:
        await ctx.message.reply("Lỗi không thể lấy dữ liệu từ mystenlab")

bot.run(TOKEN)