import sys
import discord
from discord.ext import commands
import requests
import json
import asyncio
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

def get_all_collections():
    try:
        url = f'https://nft.llama.fi/collections'
        response = requests.get(url)
        data = response.json()
        return data
    except Exception as e:
        return "Không thể lấy dữ liệu"
    
def save_to_file(data):
    with open('nft.json', 'w') as f:
        json.dump(data, f)

async def update_nft_data():
    while True:
        nft = get_all_collections()
        save_to_file(nft)
        await asyncio.sleep(300)  # 3600 seconds = 60 minutes

def get_nft_info(address):
    try:
        url = f'http api'
        response = requests.get(url)
        data = response.json()
        return data
    except Exception as e:
        return "Không thể lấy dữ liệu"
nft = get_all_collections()
print(nft)
@bot.event
async def on_ready():
    print(f'Bot đã đăng nhập với tên {bot.user}')

@bot.command(name='nftinfo')
async def bullshark_info(ctx, address):
    try:
        info = get_nft_info(address)
    
        response_message += f"NFT infor: {info}"

        await ctx.message.reply(response_message)
    except Exception as e:
        await ctx.message.reply('Đã xảy ra lỗi khi lấy dữ liệu. Vui lòng thử lại sau.')

bot.run(TOKEN)