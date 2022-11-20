import discord
import random
import datetime
from datetime import timedelta
import sqlite3
import os
import asyncio
import time
import time
from discord_webhook import DiscordWebhook, DiscordEmbed
import requests
import randomstring
from discord.ui import View
import json
from toss import check1

_TOKEN_ = ""

intents = discord.Intents.all()
bot = discord.Bot(intents=intents)
database = './id.json'

def is_expired(time):
    ServerTime = datetime.datetime.now()
    ExpireTime = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
    if ((ExpireTime - ServerTime).total_seconds() > 0):
        return False
    else:
        return True

def get_expiretime(time):
    ServerTime = datetime.datetime.now()
    ExpireTime = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
    if ((ExpireTime - ServerTime).total_seconds() > 0):
        how_long = (ExpireTime - ServerTime)
        days = how_long.days
        hours = how_long.seconds // 3600
        minutes = how_long.seconds // 60 - hours * 60
        return str(round(days)) + "일 " + str(round(hours)) + "시간 " + str(round(minutes)) + "분" 
    else:
        return False

def prime_number(number):
    if number != 1:                 
        for f in range(2, number):  
            if number % f == 0:     
                return False
    else:
        return False
    return True

def make_expiretime(days):
    ServerTime = datetime.datetime.now()
    ExpireTime = ServerTime + timedelta(days=days)
    ExpireTime_STR = (ServerTime + timedelta(days=days)).strftime('%Y-%m-%d %H:%M')
    return ExpireTime_STR

def add_time(now_days, add_days):
    ExpireTime = datetime.datetime.strptime(now_days, '%Y-%m-%d %H:%M')
    ExpireTime_STR = (ExpireTime + timedelta(days=add_days)).strftime('%Y-%m-%d %H:%M')
    return ExpireTime_STR

def nowstr():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

def get_logwebhk(serverid):
    con = sqlite3.connect("../DB/" + str(serverid) + ".db")
    cur = con.cursor()
    cur.execute("SELECT logwebhk FROM sever;")
    data = cur.fetchone()[0]
    con.close()
    return data

def get_buylogwebhk(serverid):
    con = sqlite3.connect("../DB/" + str(serverid) + ".db")
    cur = con.cursor()
    cur.execute("SELECT buylogwebhk FROM sever;")
    data = cur.fetchone()[0]
    con.close()
    return data

def get_roleid(serverid):
    con = sqlite3.connect("../DB/" + str(serverid) + ".db")
    cur = con.cursor()
    cur.execute("SELECT roleid FROM sever;")
    data = cur.fetchone()[0]
    con.close()
    if (str(data).isdigit()):
        return int(data)
    else:
        return data

@bot.event
async def on_ready():
    print("βετα Online")
    # DiscordComponents(bot)
    # while True:
    #     await bot.change_presence(activity=discord.Game(name=f"{len(bot.guilds)}개의 서버에서"))

master_ids=[]

class Panel(View):
  def __init__(self):
    super().__init__(timeout=None)

    supportServerButton = discord.ui.Button(label='바로가기', style=discord.ButtonStyle.gray, url='')
    self.add_item(supportServerButton)

@bot.slash_command(name="코드생성", description="총판 코드 생성", guilds=[])
async def 생성(ctx):
    if ctx.channel.id == :

        con = sqlite3.connect("../DB/license.db")
        cur = con.cursor()

        code = randomstring.pick(4).upper()
        code1 = randomstring.pick(4).upper()
        code2 = randomstring.pick(4).upper()
        code3 = randomstring.pick(6).upper()

        tcode = code + '-' + code1 + '-' + code2 + '-' + code3
        cur.execute("INSERT INTO license Values(?, ?, ?, ?, ?);", (tcode, 999, 0, "None", 0))

        con.commit()
        con.close()

        await ctx.respond("DM채널을 확인해주세요.")

        await ctx.author.send("**생성된 라이센스** 날짜 : **`999`** 일\n" + f"\n**{tcode}**")
    else:
        await ctx.respond(":tools: 해당 명령어는 <#1039815408229814292> 에서만 사용이 가능합니다.")

@bot.slash_command(name="서버이전", description="서버 데이터 이전")
async def 이전(ctx, 아이디:discord.Option(str, "이전할 서버아이디를 입력해주세요.")):
    if ctx.author.id == ctx.guild.owner.id:
        if (os.path.isfile("../DB/" + str(ctx.guild.id) + ".db")):
            if not (os.path.isfile("../DB/" + 아이디 + ".db")):
                e = discord.Embed(description="잠시만 기다려주세요.", color=discord.Color.green())
                e.set_author(name="DB 이전중", icon_url="https://media.discordapp.net/attachments/899122675736272976/899122684305219594/2951-loop.gif?width=160&height=160")
                gg = await ctx.respond(embed=e)
                file_oldname = os.path.join("../db/", str(ctx.guild.id) + ".db")
                file_newname_newfile = os.path.join("../db/", 아이디 + ".db")
                os.rename(file_oldname, file_newname_newfile) ## 파일이름 수정
                await asyncio.sleep(1)
                await gg.delete()
                e = discord.Embed(description="", color=discord.Color.green())
                e.set_author(name="이전완료", icon_url="https://media.discordapp.net/attachments/899122675736272976/899123054955880468/6488-dripcheckmark.gif?width=115&height=115")
                e.add_field(
                    name="DB이전이 완료되었습니다.",
                    value=f"{ctx.guild.id}.db => " + 아이디 + ".db"
                )
                await ctx.respond(embed=e)
            else:
                e=discord.Embed(description="이미 존재하는 DB입니다.", color=discord.Color.red())
                e.set_author(name="이전실패", icon_url="https://media.discordapp.net/attachments/899122675736272976/899194197305851924/3595-failed.png?width=180&height=180")
                await ctx.respond(embed=e)
                return
        else:
            e=discord.Embed(description="해당서버는 등록되지 않은 서버입니다.", color=discord.Color.red())
            e.set_author(name="이전실패", icon_url="https://media.discordapp.net/attachments/899122675736272976/899194197305851924/3595-failed.png?width=180&height=180")
            await ctx.respond(embed=e)
            return
    else:
        e=discord.Embed(description="당신은 서버의 소유자 권한이 없습니다.", color=discord.Color.red())
        e.set_author(name="이전실패", icon_url="https://media.discordapp.net/attachments/899122675736272976/899194197305851924/3595-failed.png?width=180&height=180")
        await ctx.respond(embed=e)
        return

@bot.slash_command(name="연장", description="서버 라이센스 연장")
async def 연장(ctx, 라이센스:discord.Option(str, "연장할 라이센스를 입력해주세요.")):
    if ctx.author.guild_permissions.administrator:
        con = sqlite3.connect("../DB/" + "license.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM license WHERE code == ?;", (라이센스,))
        search_result = cur.fetchone()
        con.close()
        if (search_result != None):
            if (search_result[2] == 0):
                if (os.path.isfile("../DB/" + str(ctx.guild.id) + ".db")):
                    e=discord.Embed(
                        description="잠시만 기다려주세요.",
                        color=discord.Color.green()
                    )
                    e.set_author(name="연장하는중", icon_url="https://media.discordapp.net/attachments/899122675736272976/899122684305219594/2951-loop.gif?width=160&height=160")
                    gg = await ctx.respond(embed=e)
                    con = sqlite3.connect("../DB/" + str(ctx.guild.id) + ".db")
                    cur = con.cursor()
                    cur.execute("SELECT * FROM sever;")
                    server_info = cur.fetchone()
                    if (is_expired(server_info[1])):
                        new_expiretime = make_expiretime(search_result[1])
                    else:
                        new_expiretime = add_time(server_info[1], search_result[1])
                    cur.execute("UPDATE sever SET expiredate = ?;", (new_expiretime,))
                    con.commit()
                    con.close()
                    con = sqlite3.connect("../DB/" + "license.db")
                    cur = con.cursor()
                    cur.execute("UPDATE license SET isused = ?, useddate = ?, usedby = ? WHERE code == ?;", (1, nowstr(), ctx.guild.id, 라이센스))
                    con.commit()
                    con.close()
                    await asyncio.sleep(1)
                    e=discord.Embed(
                        title="사용해주셔서 감사합니다",
                        description="연장된 기간 : **`" + str(search_result[1]) + "`** 일",
                        color=discord.Color.green()
                    )
                    e.set_author(name="연장성공", icon_url="https://media.discordapp.net/attachments/899122675736272976/899123054955880468/6488-dripcheckmark.gif?width=115&height=115")
                    await ctx.send(embed=e)
                else:
                    e=discord.Embed(description="이 명령어는 등록된 서버만 사용 가능합니다\n`-등록` 으로 등록을 먼저 해주세요.", color=discord.Color.red())
                    e.set_author(name="연장실패", icon_url="https://media.discordapp.net/attachments/899122675736272976/899194197305851924/3595-failed.png?width=180&height=180")
                    await ctx.respond(embed=e)
                    return
            else:
                e=discord.Embed(description="이 코드는 사용된 코드입니다.\n문제가 있다면 판매자에게 문의해주세요.", color=discord.Color.red())
                e.set_author(name="연장실패", icon_url="https://media.discordapp.net/attachments/899122675736272976/899194197305851924/3595-failed.png?width=180&height=180")
                await ctx.repond(embed=e)
                return
        else:
            e=discord.Embed(description="존재하지 않는 라이센스입니다.\n문제가 있다면 판매자에게 문의해주세요.", color=discord.Color.red())
            e.set_author(name="연장실패", icon_url="https://media.discordapp.net/attachments/899122675736272976/899194197305851924/3595-failed.png?width=180&height=180")
            await ctx.respond(embed=e)
            return
    else:
        e=discord.Embed(description="당신은 서버의 관리자 권한이 없습니다.", color=discord.Color.red())
        e.set_author(name="연장실패", icon_url="https://media.discordapp.net/attachments/899122675736272976/899194197305851924/3595-failed.png?width=180&height=180")
        await ctx.respond(embed=e)
        return

@bot.slash_command(name="서버등록", description="서버를 등록합니다.")
async def 서버등록(ctx, 라이센스:discord.Option(str, "이전할 서버아이디를 입력해주세요.")):
    if ctx.author.guild_permissions.administrator:
        con = sqlite3.connect("../DB/license.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM license WHERE code == ?;", (라이센스,))
        data = cur.fetchone()
        con.close()                
        if data == None:
            e=discord.Embed(description="해당 라이센스키는 없는 라이센스키 입니다.\n관리자에게 문의해주세요.", color=discord.Color.red())
            e.set_author(name="등록실패", icon_url="https://media.discordapp.net/attachments/899122675736272976/899194197305851924/3595-failed.png?width=180&height=180")
            await ctx.respond(embed=e)
            return
        if data[2] == 1:
            e=discord.Embed(description="해당 라이센스키는 이미 사용된 라이센스키 입니다.\n관리자에게 문의해주세요.", color=discord.Color.red())
            e.set_author(name="등록실패", icon_url="https://media.discordapp.net/attachments/899122675736272976/899194197305851924/3595-failed.png?width=180&height=180")
            await ctx.respond(embed=e)
            return
        if (os.path.isfile("../DB/" + str(ctx.guild.id) + ".db")):
            e=discord.Embed(description="서버는 이미 등록된 서버입니다.\n`/연장` 으로 연장해주세요.", color=discord.Color.red())
            e.set_author(name="등록실패", icon_url="https://media.discordapp.net/attachments/899122675736272976/899194197305851924/3595-failed.png?width=180&height=180")
            await ctx.respond(embed=e)
            return
        else:
            e = discord.Embed(description="", color=discord.Color.green())
            e.set_author(name="서버등록중", icon_url="https://media.discordapp.net/attachments/899122675736272976/899122684305219594/2951-loop.gif?width=160&height=160")
            gg = await ctx.respond(embed=e)
            date = data[1]
            con = sqlite3.connect("../DB/" + "license.db")
            cur = con.cursor()
            cur.execute("UPDATE license SET isused = ?, useddate = ?, usedby = ? WHERE code == ?;", (1, nowstr(), ctx.guild.id, 라이센스))
            con.commit()
            con.close()
            con = sqlite3.connect("../DB/" + str(ctx.guild.id) + ".db")
            cur = con.cursor()
            cur.execute("CREATE TABLE sever (id INTEGER, expiredate TEXT, pw TEXT, roleid INTEGER, logwebhk TEXT, buylogwebhk TEXT, updatelogwebhk TEXT, vip INTENGER, vvip INTENGER, cal INTENGER, tossid TEXT, tosscharge INTENGER, tossac TEXT);")
            con.commit()
            pw = randomstring.pick(6)
            cur.execute("INSERT INTO sever VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? , ?);", (ctx.guild.id, make_expiretime(date), pw, 0, "", "", "", 0, 0, 0, "", 0, ""))
            con.commit()
            cur.execute("CREATE TABLE owner (cid TEXT, cpw TEXT, own TEXT, bank TEXT, num INTENGER);")
            con.commit()
            cur.execute("INSERT INTO owner VALUES(?, ?, ?, ?, ?);", ("", "", "", "", 0))
            con.commit()
            cur.execute("CREATE TABLE user (id INTEGER, money INTEGER, warn INTENGER, black INTENGER, buy INTENGER, vip INTENGER, vvip INTENGER);")
            con.commit()
            cur.execute("CREATE TABLE product (name INTEGER, money INTEGER, stock TEXT);")
            con.commit()
            con.close()
            await asyncio.sleep(1)
            e = discord.Embed(
                description="서버가 정상적으로 등록되었습니다.",
                color=discord.Color.blue()
            )
            e.set_author(name="등록완료", icon_url="https://media.discordapp.net/attachments/899122675736272976/899123054955880468/6488-dripcheckmark.gif?width=115&height=115")
            e.add_field(
                name="서버 정보",
                value="서버이름 : **`" + str(ctx.guild.name) + "`**\n라이센스 기간: `"+ str(date) + "`일\n만료일: `" + make_expiretime(date) + "`\n아이디: `" +str(ctx.guild.id) + "`\n비밀번호: `" + pw + "`"
            )
            e1=discord.Embed(
                description="DM을 확인해주세요",
                color=discord.Color.blue()
            )
            e1.set_author(name="등록완료", icon_url="https://media.discordapp.net/attachments/899122675736272976/899123054955880468/6488-dripcheckmark.gif?width=115&height=115")
            await ctx.send(embed=e1)
            await ctx.author.send(
                embed=e,
                view=Panel()
            )
            return
    else:
        e=discord.Embed(description="당신은 서버의 관리자 권한이 없습니다.", color=discord.Color.red())
        e.set_author(name="조회실패", icon_url="https://media.discordapp.net/attachments/899122675736272976/899194197305851924/3595-failed.png?width=180&height=180")
        await ctx.respond(embed=e)
        return

@bot.slash_command(name="세팅")
async def 세팅(ctx):
    if ctx.author.guild_permissions.administrator:
        if (os.path.isfile("../DB/" + str(ctx.guild.id) + ".db")):
            con = sqlite3.connect("../DB/" + str(ctx.guild.id) + ".db")
            cur = con.cursor()
            cur.execute("SELECT * FROM sever;")
            cmdchs = cur.fetchone()
            con.close()
            try:
                await ctx.message.delete()
            except:
                pass

            await ctx.respond("정상적으로 세팅되었습니다", ephemeral=True)
            msg = await ctx.channel.send("이용하시려면 아래의 이모지를 클릭해주세요")
            await msg.add_reaction('⭕')

            with open(database, 'r') as f:
                data = json.loads(f.read())

            new_value = {'msg' : f'{msg.id}'}
            data[f'{ctx.channel.guild.id}'] = new_value

            with open(database, 'w') as f:
                f.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
        else:
            e=discord.Embed(description="등록되지 않은 서버입니다.\n라이센스키를 구입하여 등록 해주세요.", color=discord.Color.red())
            e.set_author(name="세팅실패", icon_url="https://media.discordapp.net/attachments/899122675736272976/899194197305851924/3595-failed.png?width=180&height=180")
            await ctx.respond(embed=e)
            return
    else:
        e=discord.Embed(description="당신은 서버의 관리자 권한이 없습니다.", color=discord.Color.red())
        e.set_author(name="세팅실패", icon_url="https://media.discordapp.net/attachments/899122675736272976/899194197305851924/3595-failed.png?width=180&height=180")
        await ctx.respond(embed=e)
        return


@bot.event
async def on_raw_reaction_add(payload):
    if not (os.path.isfile("../DB/" + str(payload.guild_id) + ".db")):
        return
    emoji, user, member, channel = payload.emoji, await bot.fetch_user(payload.user_id), payload.member, bot.get_channel(payload.channel_id)
    try:
        msg = await channel.fetch_message(payload.message_id)
    except:
        return
    data = json.loads(open(database).read())
    author = payload.user_id 
    payload.guild_id = payload.guild_id
    try:
        con = sqlite3.connect("../DB/" + str(payload.guild_id) + ".db")
    except:
        return
    if user.bot:
        return
    try:
        json_guild = data[f'{payload.guild_id}']
    except: 
        return

    cur = con.cursor()
    cur.execute("SELECT * FROM sever;")
    cmdchs = cur.fetchone()

    now = datetime.datetime.now()
    nowDatetime = now.strftime('%Y-%m-%d %H:%M')

    if not nowDatetime >= cmdchs[1]:
        if str(payload.message_id) == json_guild['msg']:
            if str(payload.emoji) == '⭕':
                con = sqlite3.connect("../DB/" + str(payload.guild_id) + ".db")
                cur = con.cursor()
                cur.execute("SELECT * FROM user WHERE id == ?;", (author,))
                user_info = cur.fetchone()
                if (user_info == None):
                    cur.execute("INSERT INTO user VALUES(?, ?, ?, ?, ?, ?, ?);", (author, 0, 0, 0, 0, 0, 0))
                    con.commit()
                await msg.clear_reactions()
                await msg.add_reaction('⭕')
                m = discord.Embed(
                    title="Auto Charging Machine",
                    description="무엇을 하시겠습니까?",
                    color=discord.Color.green()
                )
                m.add_field(
                    name="카테고리",
                    value="0️⃣ 구매\n1️⃣ 재고확인\n2️⃣ 충전\n3️⃣ 정보확인"
                )
                m.set_footer(
                    text = f"현재 자판기 서버 : {str(msg.guild.name)}"
                )
                try:
                    gh = await user.send(embed=m)
                    await gh.add_reaction("0️⃣")
                    await gh.add_reaction("1️⃣")
                    await gh.add_reaction("2️⃣")
                    await gh.add_reaction("3️⃣")
                except:
                    return
                while True:
                    def check(reaction, user):
                        return user == payload.member
                    try:
                        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
                    except asyncio.TimeoutError:
                        return

                    if (str(reaction.emoji) == '0️⃣'):
                        try:
                            await gh.delete()
                        except:
                            pass
                        con = sqlite3.connect("../DB/" + str(payload.guild_id) + ".db")
                        cur = con.cursor()
                        try:
                            cur.execute("SELECT * FROM product;")
                        except:
                            await user.send("아무런 제품이 없습니다")
                            return
                        products = cur.fetchall()

                        emoji = [ "0️⃣" ,"1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
                        nm = len(products)

                        e = discord.Embed(
                            title = "AutoCat",
                            description="제품목록입니다.",
                            color = discord.Color.green()
                        )
                        i2 = 0
                        product_names = []
                        for product in products:
                            if i2 == nm:
                                break
                            e.add_field(name = f"이모지 : {emoji[i2]}",value = f"제품 : {product[0]}", inline=False)
                            product_names.append(product[0])
                            i2 += 1

                        gg = await user.send(embed=e)

                        i = 0
                        while True:
                            if i == nm:
                                break
                            await gg.add_reaction(emoji[i])
                            i += 1

                        def check(reaction, user):
                            return user == payload.member
                        try:
                            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
                        except asyncio.TimeoutError:
                            await gg.delete()
                            return
                        offset = emoji.index(str(reaction.emoji))
                        await gg.delete()
                        product_name = product_names[offset]
                        cur.execute("SELECT * FROM product WHERE name = ?;", (product_name,))
                        product_info = cur.fetchone()
                        if (product_info != None):
                            if (str(product_info[2]) != ""):
                                e=discord.Embed(
                                    title="수량선택",
                                    description=f"아래 이모지 `📩` 를 눌러 {product_name} 제품 `1`개를 구매합니다.\n갯수를 수정하고 싶다면 `✏️` 이모지를 클릭해주세요.\n취소를 원하시면 `⛔`를 클릭해주세요.",
                                    color=discord.Color.green()
                                )
                                info_msg = await user.send(embed=e)
                                try:
                                    await info_msg.add_reaction("📩")
                                    await info_msg.add_reaction("✏️")
                                    await info_msg.add_reaction("⛔")
                                except:
                                    pass
                                def check(reaction, user):
                                    return user == payload.member
                                try:
                                    reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
                                except asyncio.TimeoutError:
                                    return

                                if str(reaction.emoji) == "⛔":
                                    await info_msg.delete()
                                    return
                                if str(reaction.emoji) == "📩":
                                    if (len(product_info[2].split("\n")) >= 1):
                                        if (int(user_info[1]) >= int(product_info[1])):
                                            e=discord.Embed(
                                                description="",
                                                color=discord.Color.green()
                                            )
                                            e.set_author(name="구매진행중", icon_url="https://media.discordapp.net/attachments/899122675736272976/899122684305219594/2951-loop.gif?width=160&height=160")
                                            await info_msg.delete()
                                            try_msg = await user.send(embed=e)
                                            stocks = product_info[2].split("\n")
                                            bought_stock = []
                                            for n in range(1):
                                                picked = random.choice(stocks)
                                                bought_stock.append(picked)
                                                stocks.remove(picked)
                                            now_stock = "\n".join(stocks)
                                            now_money = int(user_info[1]) - (int(product_info[1]))
                                            now_bought = int(user_info[2]) + (int(product_info[1]))
                                            con = sqlite3.connect("../DB/" + str(payload.guild_id) + ".db")
                                            cur = con.cursor()
                                            cur.execute("UPDATE user SET money = ?, warn = ? WHERE id == ?;", (now_money, now_bought, author))
                                            con.commit()
                                            cur.execute("UPDATE product SET stock = ? WHERE name == ?;", (now_stock, product_name))
                                            con.commit()
                                            con.close()
                                            bought_stock = "\n".join(bought_stock)
                                            if (len(bought_stock) > 1000):
                                                con = sqlite3.connect("../DB/docs.db")
                                                cur = con.cursor()
                                                docs_name = randomstring.pick(30)
                                                cur.execute("INSERT INTO docs VALUES(?, ?);", (docs_name, bought_stock))
                                                con.commit()
                                                con.close()
                                                docs_url = "rawviewer/" + docs_name
                                                try:
                                                    try:
                                                        webhook = DiscordWebhook(username="Auto Charging Machine", avatar_url="https://cdn.discordapp.com/attachments/794207652602708019/794572711376453642/4460d42506dfee4b6f7796acc1c6d604.gif", url=get_logwebhk(payload.guild_id))
                                                        eb = DiscordEmbed(title='제품 구매 로그', description='[웹 패널로 이동하기]()', color=0x7289da)
                                                        eb.add_embed_field(name='디스코드 닉네임', value=str(user.name), inline=False)
                                                        eb.add_embed_field(name='구매 제품', value=str(product_name), inline=False)
                                                        eb.add_embed_field(name='구매 코드', value='[구매한 코드 보기](' + docs_url + ')', inline=False)
                                                        webhook.add_embed(eb)
                                                        webhook.execute()
                                                    except:
                                                        pass

                                                    try:
                                                        webhook = DiscordWebhook(username="Auto Charging Machine", avatar_url="https://cdn.discordapp.com/attachments/794207652602708019/794572711376453642/4460d42506dfee4b6f7796acc1c6d604.gif", url=get_buylogwebhk(payload.guild_id))
                                                        webhook.add_embed(DiscordEmbed(description="<@" + str(author) + ">" + "님, `" + product_name + "` 제품 `" + str(buy_amount) + "`개 구매 감사합니다.", color=0x7289da))
                                                        webhook.execute()
                                                    except:
                                                        pass

                                                    try:
                                                        con = sqlite3.connect("../DB/" + str(payload.guild_id) + ".db")
                                                        cur = con.cursor()
                                                        cur.execute(f"select roleid from sever;")
                                                        data = cur.fetchone()
                                                        data1 = str(data).replace("(", "").replace(")", "").replace(",", "")
                                                        roles = discord.utils.get(payload.member.guild.roles, id=int(data1))
                                                        await user.add_roles(roles)

                                                    except:
                                                        pass

                                                    e = discord.Embed(
                                                        title="구매가 완료되었습니다",
                                                        description="이용해주셔서 감사합니다",
                                                        color=discord.Color.green()
                                                    )

                                                    e.add_field(name="구매하신 제품", value="`" + product_name + "`", inline=False).add_field(name="구매하신 코드", value='[구매한 코드 보기](' + docs_url + ')', inline=False)
                                                    e.add_field(name="구매하신 코드", value='[구매한 코드 보기](' + docs_url + ')', inline=False)
                                                    e.add_field(name="차감 금액", value="`" + str(int(product_info[1])) + "`원", inline=False)
                                                    await try_msg.edit(embed=e)
                                                except:
                                                    try:
                                                        await try_msg.delete()
                                                    except:
                                                        e=discord.Embed(
                                                            title="구매 실패",
                                                            description="제품 구매 중 알 수 없는 오류가 발생했습니다.\n샵 관리자에게 문의해주세요."
                                                        )
                                                        await try_msg.edit(embed=e)

                                            else:
                                                try:
                                                    try:
                                                        webhook = DiscordWebhook(username="Auto Charging Machine", avatar_url="https://cdn.discordapp.com/attachments/794207652602708019/794572711376453642/4460d42506dfee4b6f7796acc1c6d604.gif", url=get_logwebhk(payload.guild_id))
                                                        eb = DiscordEmbed(title='제품 구매 로그', description='[웹 패널로 이동하기]()', color=0x7289da)
                                                        eb.add_embed_field(name='디스코드 닉네임', value=str(user), inline=False)
                                                        eb.add_embed_field(name='구매 제품', value=str(product_name), inline=False)
                                                        eb.add_embed_field(name='구매 코드', value=bought_stock, inline=False)
                                                        webhook.add_embed(eb)
                                                        webhook.execute()
                                                    except:
                                                        pass

                                                    try:
                                                        webhook = DiscordWebhook(username="Auto Charging Machine", avatar_url="https://cdn.discordapp.com/attachments/794207652602708019/794572711376453642/4460d42506dfee4b6f7796acc1c6d604.gif", url=get_buylogwebhk(payload.guild_id))
                                                        webhook.add_embed(DiscordEmbed(description="<@" + str(author) + ">" + "님, `" + product_name + "` 제품 `1`개 구매 감사합니다.", color=0x7289da))
                                                        webhook.execute()
                                                    except:
                                                        pass

                                                    try:
                                                        con = sqlite3.connect("../DB/" + str(payload.guild_id) + ".db")
                                                        cur = con.cursor()
                                                        cur.execute(f"select roleid from sever;")
                                                        data = cur.fetchone()
                                                        data1 = str(data).replace("(", "").replace(")", "").replace(",", "")
                                                        roles = discord.utils.get(payload.member.guild.roles, id=int(data1))
                                                        await user.add_roles(roles)
                                                    except:
                                                        pass

                                                    e=discord.Embed(
                                                        title="구매가 완료되었습니다",
                                                        description="구매해주셔서 감사합니다",
                                                        color=discord.Color.green()
                                                    )

                                                    e.add_field(name="구매하신 제품", value="`" + product_name + "`", inline=False)
                                                    e.add_field(name="구매하신 코드", value="`" + str(bought_stock) + "`", inline=False)
                                                    e.add_field(name="차감 금액", value="`" + str(int(product_info[1])) + "`원", inline=False)
                                                    await asyncio.sleep(1)
                                                    await try_msg.delete()
                                                    await user.send(embed=e)
                                                    await user.send(f"```{str(bought_stock)}```")
                                                    return
                                                except:
                                                    try:
                                                        await try_msg.delete()
                                                    except:
                                                        pass
                                                    e=discord.Embed(
                                                        title="제품 구매 실패",
                                                        description="제품 구매 중 알 수 없는 오류가 발생했습니다.\n샵 관리자에게 문의해주세요.",
                                                        color=discord.Color.red()
                                                    )
                                                    await user.send(embed=e)
                                                    return
                                        else:
                                            e=discord.Embed(
                                                title="구매 실패",
                                                description="구매할 돈을 소지하지않고 있습니다",
                                                color=discord.Color.red()
                                            )
                                            await info_msg.delete()
                                            await user.send(embed=e)
                                            return
                                elif str(reaction.emoji) == "✏️":
                                    await info_msg.delete()
                                    e=discord.Embed(
                                        title="수량 설정하기",
                                        description="구매하실 수량을 작성해주세요.",
                                        color=discord.Color.green()
                                    )
                                    gg = await user.send(embed=e)
                                    def check(m):
                                        return user == m.author
                                    try:
                                        msg = await bot.wait_for("message", timeout=60.0, check=check)
                                    except asyncio.TimeoutError:
                                        try:
                                            await gg.delete()
                                        except:
                                            pass
                                        e=discord.Embed(
                                            title="시간초과",
                                            description="처음부터 다시 시도해주세요",
                                            color=discord.Color.red()
                                        )
                                        await bot.get_user(author).send(embed=e)
                                        return None
                                    if not ((msg.content.isdigit()) and (msg.content != "0")):
                                        e=discord.Embed(
                                            title="구매실패",
                                            description="수량은 숫자로만 입력해주세요",
                                            color=discord.Color.red()
                                        )
                                        await bot.get_user(author).send(embed=e)
                                        return None
                                    buy_amount = int(msg.content)
                                    if (len(product_info[2].split("\n")) >= buy_amount):
                                        if (int(user_info[1]) >= int(product_info[1] * buy_amount)):
                                            await gg.delete()
                                            e=discord.Embed(
                                                description="",
                                                color=discord.Color.green()
                                            )
                                            e.set_author(name="구매진행중", icon_url="https://media.discordapp.net/attachments/899122675736272976/899122684305219594/2951-loop.gif?width=160&height=160")
                                            try_msg = await bot.get_user(author).send(embed=e)
                                            stocks = product_info[2].split("\n")
                                            bought_stock = []
                                            for n in range(buy_amount):
                                                picked = random.choice(stocks)
                                                bought_stock.append(picked)
                                                stocks.remove(picked)
                                            now_stock = "\n".join(stocks)
                                            now_money = int(user_info[1]) - (int(product_info[1]) * buy_amount)
                                            now_bought = int(user_info[2]) + (int(product_info[1]) * buy_amount)
                                            con = sqlite3.connect("../DB/" + str(payload.guild_id) + ".db")
                                            cur = con.cursor()
                                            cur.execute("UPDATE user SET money = ?, warn = ? WHERE id == ?;", (now_money, now_bought, author))
                                            con.commit()
                                            cur.execute("UPDATE product SET stock = ? WHERE name == ?;", (now_stock, product_name))
                                            con.commit()
                                            con.close()
                                            bought_stock = "\n".join(bought_stock)
                                            if (len(bought_stock) > 1000):
                                                con = sqlite3.connect("../DB/docs.db")
                                                cur = con.cursor()
                                                docs_name = randomstring.pick(30)
                                                cur.execute("INSERT INTO docs VALUES(?, ?);", (docs_name, bought_stock))
                                                con.commit()
                                                con.close()
                                                docs_url = "rawviewer/" + docs_name
                                                try:
                                                    try:
                                                        webhook = DiscordWebhook(username="Auto Charging Machine", avatar_url="https://cdn.discordapp.com/attachments/794207652602708019/794572711376453642/4460d42506dfee4b6f7796acc1c6d604.gif", url=get_logwebhk(payload.guild_id))
                                                        eb = DiscordEmbed(title='제품 구매 로그', description='[웹 패널로 이동하기]()', color=0x7289da)
                                                        eb.add_embed_field(name='디스코드 닉네임', value=str(user.name), inline=False)
                                                        eb.add_embed_field(name='구매 제품', value=str(product_name), inline=False)
                                                        eb.add_embed_field(name='구매 코드', value='[구매한 코드 보기](' + docs_url + ')', inline=False)
                                                        webhook.add_embed(eb)
                                                        webhook.execute()
                                                    except:
                                                        pass

                                                    try:
                                                        webhook = DiscordWebhook(username="Auto Charging Machine", avatar_url="https://cdn.discordapp.com/attachments/794207652602708019/794572711376453642/4460d42506dfee4b6f7796acc1c6d604.gif", url=get_buylogwebhk(payload.guild_id))
                                                        webhook.add_embed(DiscordEmbed(description="<@" + str(author) + ">" + "님, `" + product_name + "` 제품 `" + str(buy_amount) + "`개 구매 감사합니다.", color=0x7289da))
                                                        webhook.execute()
                                                    except:
                                                        pass

                                                    try:
                                                        con = sqlite3.connect("../DB/" + str(payload.guild_id) + ".db")
                                                        cur = con.cursor()
                                                        cur.execute(f"select roleid from sever;")
                                                        data = cur.fetchone()
                                                        data1 = str(data).replace("(", "").replace(")", "").replace(",", "")
                                                        await user.add_roles(data1)
                                                        roles = discord.utils.get(payload.member.guild.roles, id=int(data1))
                                                        await user.add_roles(roles)
                                                    except:
                                                        pass

                                                    e = discord.Embed(
                                                        title="구매가 완료되었습니다",
                                                        description="이용해주셔서 감사합니다",
                                                        color=discord.Color.green()
                                                    )

                                                    e.add_field(name="구매하신 제품", value="`" + product_name + "`", inline=False).add_field(name="구매하신 코드", value='[구매한 코드 보기](' + docs_url + ')', inline=False)
                                                    e.add_field(name="구매하신 코드", value='[구매한 코드 보기](' + docs_url + ')', inline=False)
                                                    e.add_field(name="차감 금액", value="`" + str(int(product_info[1]) * buy_amount) + "`원", inline=False)
                                                    await try_msg.edit(embed=e)
                                                except:
                                                    try:
                                                        await try_msg.delete()
                                                    except:
                                                        e=discord.Embed(
                                                            title="구매 실패",
                                                            description="제품 구매 중 알 수 없는 오류가 발생했습니다.\n샵 관리자에게 문의해주세요."
                                                        )
                                                        await try_msg.edit(embed=e)
                                                        return

                                            else:
                                                try:
                                                    try:
                                                        webhook = DiscordWebhook(username="Auto Charging Machine", avatar_url="https://cdn.discordapp.com/attachments/794207652602708019/794572711376453642/4460d42506dfee4b6f7796acc1c6d604.gif", url=get_logwebhk(payload.guild_id))
                                                        eb = DiscordEmbed(title='제품 구매 로그', description='[웹 패널로 이동하기]()', color=0x7289da)
                                                        eb.add_embed_field(name='디스코드 닉네임', value=str(user), inline=False)
                                                        eb.add_embed_field(name='구매 제품', value=str(product_name), inline=False)
                                                        eb.add_embed_field(name='구매 코드', value=bought_stock, inline=False)
                                                        webhook.add_embed(eb)
                                                        webhook.execute()
                                                    except:
                                                        pass

                                                    try:
                                                        webhook = DiscordWebhook(username="Auto Charging Machine", avatar_url="https://cdn.discordapp.com/attachments/794207652602708019/794572711376453642/4460d42506dfee4b6f7796acc1c6d604.gif", url=get_buylogwebhk(payload.guild_id))
                                                        webhook.add_embed(DiscordEmbed(description="<@" + str(author) + ">" + "님, `" + product_name + "` 제품 `" + str(buy_amount) + "`개 구매 감사합니다.", color=0x7289da))
                                                        webhook.execute()
                                                    except:
                                                        pass
                                                    try:
                                                        con = sqlite3.connect("../DB/" + str(payload.guild_id) + ".db")
                                                        cur = con.cursor()
                                                        cur.execute(f"select roleid from sever;")
                                                        data = cur.fetchone()
                                                        data1 = str(data).replace("(", "").replace(")", "").replace(",", "")
                                                        await user.add_roles(data1)
                                                        roles = discord.utils.get(payload.member.guild.roles, id=int(data1))
                                                        await user.add_roles(roles)
                                                    except:
                                                        pass

                                                    e=discord.Embed(
                                                        title="구매가 완료되었습니다",
                                                        description="구매해주셔서 감사합니다",
                                                        color=discord.Color.green()
                                                    )

                                                    e.add_field(name="구매하신 제품", value="`" + product_name + "`", inline=False)
                                                    e.add_field(name="구매하신 코드", value="`" + str(bought_stock) + "`", inline=False)
                                                    e.add_field(name="차감 금액", value="`" + str(int(product_info[1]) * buy_amount) + "`원", inline=False)
                                                    await asyncio.sleep(1)
                                                    await try_msg.delete()
                                                    await user.send(embed=e)
                                                    await user.send(f"```{str(bought_stock)}```")
                                                    return
                                                except:
                                                    try:
                                                        await try_msg.delete()
                                                    except:
                                                        pass
                                                    e=discord.Embed(
                                                        title="제품 구매 실패",
                                                        description="제품 구매 중 알 수 없는 오류가 발생했습니다.\n샵 관리자에게 문의해주세요.",
                                                        color=discord.Color.red()
                                                    )
                                                    await gh.edit(embed=e)
                                                    return
                                        else:
                                            e=discord.Embed(
                                                title="구매 실패",
                                                description="구매할 돈을 소지하지않고 있습니다",
                                                color=discord.Color.red()
                                            )
                                            try:
                                                await info_msg.delete()
                                            except:
                                                pass
                                            await user.send(embed=e)
                                            return
                                    else:
                                        e=discord.Embed(
                                            title="구매 실패",
                                            description="재고가 부족합니다.",
                                            color=discord.Color.red()
                                        )
                                        try:
                                            await info_msg.delete()
                                        except:
                                            pass
                                        await user.send(embed=e)
                                        return
                            else:
                                e=discord.Embed(
                                    title="구매 실패",
                                    description="재고가 부족합니다.",
                                    color=discord.Color.red()
                                )
                                try:
                                    await info_msg.delete()
                                except:
                                    pass
                                await user.send(embed=e)
                                return
                    elif (str(reaction.emoji) == '1️⃣'):
                        con = sqlite3.connect("../DB/" + str(payload.guild_id) + ".db")
                        cur = con.cursor()
                        cur.execute("SELECT * FROM product;")
                        products = cur.fetchall()
                        products1 = cur.fetchone()
                        con.close()
                        if len(products) == 0:
                            e=discord.Embed(
                                title=f"불러오기 실패",
                                description="해당 서버에 등록된 제품이 존재하지 않습니다.",
                                color=discord.Color.red()
                            )
                            try:
                                await gh.delete()
                            except:
                                pass
                            return await user.send(embed=e)
                        e=discord.Embed(
                            title=f"제품목록입니다.",
                            description="",
                            color=discord.Color.green()
                        )
                        for product in products:
                            if (product[2] != ""):
                                e.add_field(name="제품명 : " + product[0], value="가격: `" + str(product[1]) + "`원\n재고: `" + str(len(product[2].split("\n"))) + "`개", inline=False)
                            else:
                                e.add_field(name="제품명 : " + product[0], value="가격: " + str(product[1]) + "원\n재고: `부족`", inline=False)
                        try:
                            await gh.delete()
                        except:
                            pass
                        await user.send(embed=e)
                        break
                    elif str(reaction.emoji) == "2️⃣":
                        con = sqlite3.connect("../DB/" + str(payload.guild_id) + ".db")
                        cur = con.cursor()
                        cur.execute("SELECT * FROM user WHERE id == ?;", (user.id,))
                        user_info = cur.fetchone()
                        cur.execute("SELECT * FROM owner;")
                        server_info = cur.fetchone()
                        cur.execute("SELECT * FROM sever;")
                        sever_info = cur.fetchone()
                        con.close()
                        e = discord.Embed(
                            title="충전신청",
                            description="__**충전방식을 선택해주세요**__.\n💵 - `문화상품권 충전`\n💳 - `계좌 충전`\n⛔ - `충전 취소`",
                            color=discord.Color.green()
                        )
                        await gh.delete()
                        jk22 = await user.send(embed=e)
                        await jk22.add_reaction("💵")
                        await jk22.add_reaction("💳")
                        await jk22.add_reaction("⛔")
                        def check(reaction, user):
                            return user == payload.member
                        try:
                            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
                        except asyncio.TimeoutError:
                            return await jk22.delete()
                        def check(m):
                            return user == m.author
                        if str(reaction.emoji) == "⛔":
                            return await jk22.delete()
                        elif str(reaction.emoji) == "💳":
                            if (sever_info[8] != "" and sever_info[10] != ""):
                                e = discord.Embed(
                                    title = "계좌충전",
                                    description="`입금자명`을 작성해주세요.",
                                    color=discord.Color.green()
                                )
                                await jk22.delete()
                                jk33 = await user.send(embed=e)
                                try:
                                    msgg = await bot.wait_for("message", timeout=60.0, check=check)
                                except asyncio.TimeoutError:
                                    await jk33.delete()
                                    return
                                if msgg:
                                    e = discord.Embed(
                                        title = "계좌충전",
                                        description="`입금금액`을 작성해주세요.",
                                        color=discord.Color.green()
                                    )
                                    await jk33.delete()
                                    jk44 = await user.send(embed=e)
                                    try:
                                        msggg = await bot.wait_for("message", timeout=60.0, check=check)
                                    except asyncio.TimeoutError:
                                        await jk44.delete()
                                        return
                                    if msggg:
                                        e= discord.Embed(
                                            title = "계좌충전",
                                            description=f"입금은행 : `토스뱅크`\n입금계좌 : **{sever_info[10]}**\n입금자명 : **{msgg.content}**\n입금금액 : **{msggg.content}**\n입금 후 아래의 이모지를 클릭해주세요.",
                                            color = discord.Color.green()
                                        )
                                        await jk44.delete()
                                        jk55 = await user.send(embed=e)
                                        await jk55.add_reaction("✅")
                                        def check(reaction, user):
                                            return user == payload.member
                                        try:
                                            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
                                        except asyncio.TimeoutError:
                                            return await jk55.delete()
                                        if str(reaction.emoji == "✅"):
                                            gg = check1(msgg.content, int(msggg.content), sever_info[9])
                                            print(gg)
                                            if gg["result"] == True:
                                                cur.execute("UPDATE user SET money = money + ? WHERE id == ?;", (int(msggg.content), user.id))
                                                con.commit()
                                                e = discord.Embed(
                                                    title = "충전성공",
                                                    description=f"성공적으로 계좌충전을 하였습니다.\n충전금액 : **{(msggg.content)}**원\n이용해주셔서 감사합니다.",
                                                    color=discord.Color.green()
                                                )
                                                await jk55.delete()
                                                return await user.send(embed=e)
                                            else:
                                                e = discord.Embed(
                                                    title = "충전실패",
                                                    description=f"계좌충전에 실패하였습니다.\n사유 : **{gg['msg']}**",
                                                    color=discord.Color.red()
                                                )
                                                await jk55.delete()
                                                return await user.send(embed=e)
                        elif str(reaction.emoji) == "💵":
                            if (server_info[0] != "" and server_info[1] != ""):
                                if (user_info != None):
                                    def check(m):
                                        return user == m.author
                                    try:
                                        e = discord.Embed(
                                            title="문화상품권 충전방법",
                                            description="문화상품권 코드를 `-`을 포함해서 입력해주세요.",
                                            color=discord.Color.green()
                                        )
                                        await jk22.delete()
                                        jk21 = await user.send(embed=e)
                                    except:
                                        return

                                    try:
                                        msg = await bot.wait_for("message", timeout=60.0, check=check)
                                    except asyncio.TimeoutError:
                                        try:
                                            e = discord.Embed(
                                                title="문화상품권 충전 실패",
                                                description="시간 초과되었습니다.",
                                                color=discord.Color.red()
                                            )
                                            await jk21.edit(embed=e)
                                        except:
                                            pass
                                        return None

                                    if msg.content: 
                                        try:
                                            jsondata = {"id" : str(server_info[0]), "pw" : str(server_info[1]), "pin" : msg.content, "token" : "pIwDtDPmYDlUg43jJXJ8"}
                                            res = requests.post("http://sywebservice.com:100/api", json=jsondata)
                                            if (res.status_code != 200):
                                                raise TypeError
                                            else:
                                                print(str(res))
                                                res = res.json()
                                        except:
                                            try:
                                                e = discord.Embed(
                                                    title="문화상품권 충전 실패",
                                                    description="일시적인 서버 오류입니다.\n잠시 후 다시 시도해주세요.",
                                                    color=discord.Color.red()
                                                )
                                                await jk21.delete()
                                                await bot.get_user(author).send(embed=e)
                                            except:
                                                pass
                                            return None

                                        if (res["result"] == True):
                                            culture_amount = int(res["amount"])
                                            cur = con.cursor()
                                            cur.execute("SELECT * FROM user WHERE id == ?;", (msg.author.id,))
                                            user_info = cur.fetchone()
                                            current_money = int(user_info[1])
                                            now_money = current_money + culture_amount
                                            cur.execute("UPDATE user SET money = ? WHERE id == ?;", (now_money, msg.author.id))
                                            con.commit()
                                            con.close()
                                            try:
                                                e=discord.Embed(
                                                    title="문화상품권 충전 성공",
                                                    description="핀코드: `" + msg.content + "`\n금액: `" + str(culture_amount) + "`원\n충전 후 금액: `" + str(now_money) + "`원",
                                                    color=discord.Color.green()
                                                )
                                                await jk21.edit(embed=e)
                                                try:
                                                    webhook = DiscordWebhook(username="Auto Charging Machine", avatar_url="https://cdn.discordapp.com/attachments/794207652602708019/794572711376453642/4460d42506dfee4b6f7796acc1c6d604.gif", url=get_logwebhk(payload.guild_id))
                                                    eb = DiscordEmbed(title='문화상품권 충전 성공', description='[웹 패널로 이동하기]()', color=0x7289da)
                                                    eb.add_embed_field(name='디스코드 닉네임', value=str(msg.author), inline=False)
                                                    eb.add_embed_field(name='핀 코드', value=str(msg.content), inline=False)
                                                    eb.add_embed_field(name='충전 금액', value=str(res["amount"]), inline=False)
                                                    webhook.add_embed(eb)
                                                    webhook.execute()
                                                except:
                                                    pass
                                            except:
                                                pass
                                        else:
                                            try:
                                                e.set_author(name="충전실패", icon_url="https://media.discordapp.net/attachments/899122675736272976/899194197305851924/3595-failed.png?width=180&height=180")
                                                e=discord.Embed(
                                                    title="문화상품권 충전 실패",
                                                    description="" + res["reason"] + "",
                                                    color=discord.Color.red()
                                                )
                                                await jk21.delete()
                                                await user.send(embed=e)
                                                try:
                                                    webhook = DiscordWebhook(username="Auto Charging Machine", avatar_url="https://cdn.discordapp.com/attachments/794207652602708019/794572711376453642/4460d42506dfee4b6f7796acc1c6d604.gif", url=get_logwebhk(payload.guild_id))
                                                    eb = DiscordEmbed(title='문화상품권 충전 실패', description='[웹 패널로 이동하기]()', color=0xff0000)
                                                    eb.add_embed_field(name='디스코드 닉네임', value=str(msg.author), inline=False)
                                                    eb.add_embed_field(name='핀 코드', value=str(msg.content), inline=False)
                                                    eb.add_embed_field(name='실패 사유', value=res["reason"], inline=False)
                                                    webhook.add_embed(eb)
                                                    webhook.execute()
                                                except Exception as e:
                                                    return
                                            except:
                                                pass
                                    else:
                                        e=discord.Embed(
                                            title="충전 실패",
                                            description="핀번호는 `-` 를 포함해서 보내주세요",
                                            color=discord.Color.red()
                                        )
                                        await user.send(embed=e)
                                        return
                                        
                                else:
                                    e=discord.Embed(
                                        title="문화상품권 충전 실패",
                                        description="먼저 가입해주세요",
                                        color=discord.Color.red()
                                    )
                                    await jk22.delete()
                                    await user.send(embed=e)
                            else:
                                e=discord.Embed(
                                    title="문화상품권 충전 실패",
                                    description="충전 기능이 비활성화되어 있습니다.\n샵 관리자에게 문의해주세요."
                                )
                                await jk22.delete()
                                await user.send(embed=e)
                                break
                    elif (str(reaction.emoji) == "3️⃣"):
                        con = sqlite3.connect("../DB/" + str(payload.guild_id) + ".db")
                        cur = con.cursor()
                        cur.execute("SELECT * FROM user WHERE id == ?;", (author,))
                        user_info = cur.fetchone()
                        con.close()
                        try:
                            await gh.delete()
                        except:
                            pass
                        # e=discord.Embed(
                        #     description="잠시만 기다려주세요",
                        #     color=discord.Color.green()
                        # )
                        # e.set_author(name="유저 조회중", icon_url="https://media.discordapp.net/attachments/899122675736272976/899122684305219594/2951-loop.gif?width=160&height=160")
                        # jj = await user.send(embed=e)
                        if user_info[3] > 2:
                            j = "O"
                        else:
                            j = "X"
                        if user.bot:
                            return
                        if user_info[2] == 1:
                            j1 = "구매자"
                        elif user_info[4] == 0:
                            j1 = "비구매자"
                        elif user_info[5] == 1:
                            j1 = "VIP"
                        elif user_info[6] == 1:
                            j1 = "VVIP"
                        e=discord.Embed(
                            title=f"{user.name}님의 정보",
                            description=f"현재 자판기 : {str(msg.guild.name)} \n유저 ID: `" + str(author) + "`\n보유 금액: `" + str(user_info[1]) + "`원\n누적 금액: `" + str(user_info[2]) + "`원\n블랙여부: `" + j + f"`\n등급 : `{j1}`",
                            color=discord.Color.green()
                        )
                        e.set_author(name="조회성공", icon_url="https://media.discordapp.net/attachments/899122675736272976/899123054955880468/6488-dripcheckmark.gif?width=115&height=115")
                        await user.send(embed=e)
                        break
            else:
                await msg.clear_reactions()
                await msg.add_reaction('<:102658E53E3941588D1B03C26018BDD8:908342891561242644>')
                return
        else:
            return

bot.run(_TOKEN_)