import discord
import config

_client = discord.Client()
#_startup = str(__import__(datetime).datetime.now())

@_client.event
async def on_ready():
    print(f"Login successfull! You logged in as {_client.user}")

def report_parse(reportmsg):
    msg = reportmsg
    if reportmsg.startswith("Репорт") == False: return ["Error", "Message is not a report", None]
    else: 
        msglist = msg.split("\n")
        msglist.remove("Репорт")
        try:
            tryval = msglist[4]
        except Exception:
            return ["Error", "Message is not a report", None]
        return msglist

async def log(logmessage):
    logchannel = _client.get_channel(config.logchannel)
    await logchannel.send(logmessage)
    await _client.get_channel(841814020235460689).send(logmessage)
    print(logmessage)

# Репорт
# <Сообщение>
# <Тип нарушения>
# <Наказание>
# <Игрок>
# <Модератор>
# <Важность>
def struct_embed(report, message):
    color = 0x70b4e9
    try:
        weight = int(report[4])
    except Exception:
        weight = -1
    else:
        weight = int(report[4])

    if weight == 1:
        color = 0xafe970

    elif weight == 2:
        color = 0xe9da70

    elif weight == 3:
        color = 0xe97f70

    else:
        color = 0x70b4e9
        weight = "?"


    embedd=discord.Embed(title=f"**Репорт от {message.author}**", description=report[0], color=color)
    embedd.add_field(name="Тип нарушения", value=report[1], inline=True)
    embedd.add_field(name="Наказание", value=report[2], inline=True)
    embedd.add_field(name="Игрок", value=report[3], inline=True)
    embedd.add_field(name="Важность", value=weight, inline=True)
    #embedd.set_footer(text=f"Номер: -1")
    return embedd
global adm
adm = False

@_client.event
async def on_message(message):

    if message.content.startswith("#IGNORED"):
        return
    
    reportchannel = _client.get_channel(config.reportchannel)
    
    if message.author == _client.user: return


    if message.channel.type == discord.ChannelType.private: return
    
    #if config.respect_admin: adm = message.author.guild_permissions.administrator
    if config.respect_admin: adm = message.author.display_name.startswith("✦")
    
    await log(f"Получено сообщение: **{message.content}**\nОт: **{message.author}**\nВ: **<#{message.channel.id}>**")
    
    if message.content.startswith("Бот, иди нахуй"):
        await log(f"{message.author.mention} послал бота нахуй и был послан нахуй в ответ! ВСЕ ЧЕСТНО!!!")
        await message.channel.send(f"{message.author.mention}, нет сам иди нахуй")

    if message.channel is reportchannel:
        returnval = report_parse(str(message.content))
        if returnval == ["Error", "Message is not a report", None]:
            if adm == False: await log(f"В репортах обнаружен инородный обьект! Вот он:\n{message.content}"); return
        else:
            await message.channel.send(embed=struct_embed(returnval, message))
            await log(f"Жалоба:\n{str(returnval)}")

_client.run(config.token)