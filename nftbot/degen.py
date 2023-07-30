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
        url = f'https://quests.mystenlabs.com/api/trpc/user?batch=1&input={{"0": {{"address": "{address}"}}}}'
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
        num_commands_de_sui_flip = result['numCommandsDeSuiFlip']
        num_commands_ethos8192 = result['numCommandsEthos8192']
        num_commands_journey_to_mount_sogol = result['numCommandsJourneyToMountSogol']
        num_commands_mini_miners = result['numCommandsMiniMiners']

        response_message = f"**Score:** {score}\n**Bot:** {bot_status}\n**Rank:** {rank}\n**Reward:** {reward}\n"
        response_message += f"**NumCommandsDeSuiFlip:** {num_commands_de_sui_flip}\n"
        response_message += f"**NumCommandsEthos8192:** {num_commands_ethos8192}\n"
        response_message += f"**NumCommandsJourneyToMountSogol:** {num_commands_journey_to_mount_sogol}\n"
        response_message += f"**NumCommandsMiniMiners:** {num_commands_mini_miners}"

        await ctx.message.reply(response_message)
    except Exception as e:
        await ctx.message.reply('Đã xảy ra lỗi khi lấy dữ liệu. Vui lòng thử lại sau.')

bot.run(TOKEN)