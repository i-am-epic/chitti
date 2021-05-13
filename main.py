import discord
import os
import requests
import json
import praw
import random
from http_alive import keep_alive
from discord.ext import commands
import time

print("hekkk")

client = commands.Bot(
    command_prefix=["ch ", "Ch ", "chitti ", "Chitti ", "CH "],
    description="This is a Helper Bot")
token1 = os.environ['token']
rcid = os.environ['rcid']
rcs = os.environ['rcs']
rusername = os.environ['rusername']
trivia_key = os.environ['trivia_key']
rp = os.environ['rp']
yt_api = os.environ['yt_api']
ox_id = os.environ['ox_id']
ox_key = os.environ["ox_key"]
language = "en-gb"

reddit = praw.Reddit(client_id=rcid,
                     client_secret=rcs,
                     username=rusername,
                     password=rp,
                     user_agent="pypraw",
                     check_for_async=False)


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]["q"] + "  -" + json_data[0]["a"]
    return quote


def get_age_name(name):
    response = requests.get(f"https://api.agify.io/?name={name}")
    json_data = json.loads(response.text)
    age = json_data["age"]
    if age == None:
        age = random.randint(1, 93)
    elif age > 21:
        age += random.randint(-15, 10)
    return age


def box_color(r):
    if r < 4:
        b = "🟪"
    elif r > 6:
        b = "🟥"
    else:
        b = "🟨"
    return b


def get_yt_url(search, n=0):
    response = requests.get(
        f"https://youtube.googleapis.com/youtube/v3/search?q={search}&key={yt_api}"
    )
    json_data = json.loads(response.text)
    id = json_data["items"][n]["id"]["videoId"]
    url = f"https://www.youtube.com/watch?v={id}"
    return url, n


def get_gender(name):
    response = requests.get(f"https://api.genderize.io/?name={name}")
    json_data = json.loads(response.text)
    gender = str(json_data["gender"]) + " of " + str(
        (json_data["probability"] * 100) // 1) + "%."
    return gender


def get_country(name):
    response = requests.get(f"https://api.nationalize.io/?name={name}")
    json_data = json.loads(response.text)
    country = str(json_data["country"])
    country = list(eval(country))

    country1 = country[0]["country_id"] + " of " + str(
        (country[0]["probability"] * 100) //
        1) + "%.\n" + country[1]["country_id"] + " of " + str(
            (country[1]["probability"] * 100) //
            1) + "%.\n" + country[2]["country_id"] + " of " + str(
                (country[2]["probability"] * 100) // 1) + "%.\n"

    return country1


def get_quiz():
    r = requests.get(
        "https://quizapi.io/api/v1/questions?apiKey=jDcR7fmeEE1MlYDudAMICPMjjk4K46F3IDnWjAxN"
    )
    json_data = json.loads(r.text)
    print(r)
    return json_data


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Game("ch help"))
    print("Bots up and running as {0.user}".format(client))


@client.event
async def on_command_error(ctx,error):
  if isinstance(error,commands.CommandNotFound):
    await ctx.send("That command don't exist")
  await ctx.send(f"Error : {error}")



@client.event
async def on_member_join(ctx, *, member):
    print(f"Welcome {member} to the server")
    await ctx.send(f"Welcome {member} to the server")


@client.command(aliases=[
    "8ball", "can", "?", "will", "is", "should", "would", "could", "8b"
],
                pass_context=True)
async def _8ball(ctx, *message):
    response = [
        "It is certain.", "It is decidedly so.", "Without a doubt.",
        "Yes - definitely.", "You may rely on it.", "As I see it, yes.",
        "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
        "Reply hazy, try again.", "Ask again later.",
        "Better not tell you now.", "Cannot predict now.",
        "Concentrate and ask again.", "Don't count on it.", "My reply is no.",
        "My sources say no.", "Outlook not so good.", "Very doubtful."
    ]
    mesg = ""
    for m in message:
        mesg += " " + str(m)
    text = random.choice(response)
    text = f"{ctx.message.author.name}:  {mesg}\nchitti says:  {text}"
    await ctx.channel.purge(limit=1)
    em = discord.Embed(title=text)
    await ctx.send(embed=em)


@client.event
async def on_member_remove(ctx, member):
    print(f"{member} left us")
    await ctx.send(f"{member} left us")


@client.command()
async def age(ctx, member):
    await ctx.channel.send(get_age_name(member))


@client.command()
async def gender(ctx, member):
    await ctx.channel.send(get_gender(member))


@client.command()
async def country(ctx, member):
    await ctx.channel.send(get_country(member))


@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=10):
    await ctx.channel.send(
        "Make sure bot has message moderation permission, if not add a role with the permisiion"
    )
    await ctx.channel.purge(limit=amount + 2)


@client.command()
@commands.has_permissions(manage_messages=True, kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)


@client.command()
@commands.has_permissions(manage_messages=True, ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)


@client.command()
@commands.has_permissions(manage_messages=True, ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    banned_name, banned_hash = member.split('#')
    for banned in banned_users:
        user = banned.user
        if (user.name, user.discriminator) == (banned_name, banned_hash):

            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned.{user.mention}")
            return


@client.command()
async def f(ctx, mention):
    if mention == None: mention = ctx.author
    await ctx.channel.send(f"F u {mention}")


@client.command(aliases=["reddit", "r", "subreddit", "sr"])
async def meme(ctx, subrdt="meme"):
    subreddit = reddit.subreddit(subrdt)
    all_content = []
    top = subreddit.new(limit=10)
    for content in top:
        all_content.append(content)

    random_content = random.choice(all_content)
    title = random_content.title
    url = random_content.url
    em = discord.Embed(title=title)
    em.set_image(url=url)
    await ctx.send(embed=em)


@client.command(aliases=["quiz", "test", "Quiz", "Trivia"])
async def trivia(ctx):
    json_data = get_quiz()
    await ctx.send(json_data)

    em = discord.Embed(title="QUIZ", color=discord.Color.blue())
    """ authentication error
    for json_data in json_data:
    q = json_data["id"]+". "+json_data["question"]
    em.set_discription(name=q)
    d = json_data["description"]
    if d=="null":
      d = ""
    em.add_filed(name="                                   ", inline=False)
    em.add_filed(name="Options", inline=False)
    em.add_filed(value=f'A . {json_data["answers"]["answer_a"]}', inline=False)
    em.add_filed(value=f'B . {json_data["answers"]["answer_b"]}', inline=False)
    em.add_filed(value=f'C . {json_data["answers"]["answer_c"]}', inline=False)
    em.add_filed(value=f'D . {json_data["answers"]["answer_d"]}', inline=False)
    em.add_filed(value=f'E . {json_data["answers"]["answer_e"]}', inline=False)
    em.add_filed(value=f'F . {json_data["answers"]["answer_f"]}', inline=False)"""
    await ctx.send(embed=em)


@client.command()
async def rstart(ctx, subrdt="meme", times=1, slow=30):
    subreddit = reddit.subreddit(subrdt)
    all_content = []
    top = subreddit.top(limit=times * 4)
    i = 1
    message = await ctx.send("Hold on, finding best of the best......")

    for content in top:
        await message.edit(
            content=f"Hold on, finding best of the best......{i//4}/{times}")
        all_content.append(content)
        i = i + 1
    await ctx.channel.purge(limit=1)

    for i in range(times):
        random_content = random.choice(all_content)
        title = random_content.title
        url = random_content.url
        em = discord.Embed(title=title)
        em.set_image(url=url)
        await ctx.send(embed=em)
        time.sleep(slow)


@client.command(aliases=["t", "T"])
async def toss(ctx):
    options = ["Heads", "Tails"]
    c = random.choice(options)
    await ctx.send(c)


@client.command(aliases=["", "g", "wiki"])
async def google(ctx, *, search):
    word_id = search
    url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + language + "/" + word_id.lower(
    )
    r = requests.get(url, headers={"app_id": ox_id, "app_key": ox_key})
    json_data_def = json.loads(r.text)["results"][0]["lexicalEntries"][0][
        "entries"][0]["senses"][0]["definitions"][0]
    json_data_id = json.loads(r.text)["id"]
    json_data_ex = json.loads(r.text)["results"][0]["lexicalEntries"][0][
        "entries"][0]["senses"][0]["examples"][0]["text"]
    em = discord.Embed(title=json_data_id,
                       description=json_data_def,
                       color=discord.Color.blue())
    em.set_author(name=ctx.author.display_name,
                  url="https://twitter.com/nikkivizzz_nv",
                  icon_url=ctx.author.avatar_url)
    em.set_thumbnail(
        url=
        "https://is4-ssl.mzstatic.com/image/thumb/Purple118/v4/d2/fc/04/d2fc040a-7171-c726-5136-d6416cd85ac4/AppIcon-0-1x_U007emarketing-0-0-85-220-0-7.png/1200x630wa.png"
    )
    em.add_field(name="Example", value=json_data_ex, inline=False)

    await ctx.send(embed=em)


@client.command()
async def ping(ctx):
    await ctx.send(f"{client.latency * 1000}ms")


@client.command()
async def inspire(ctx):
    await ctx.send(get_quote())


@client.command(aliases=["gaymeter", "isgay"])
async def gay(ctx, name):
    r = random.randint(0, 10)
    b = box_color(r)
    strin = r * b + (10 - r) * "⬛" + " " + str(r * 10) + "%"
    await ctx.send(strin)


@client.command(aliases=["simpmeter", "issimp"])
async def simp(ctx, name):
    r = random.randint(0, 10)
    b = box_color(r)

    strin = r * b + (10 - r) * "⬛" + " " + str(r * 10) + "%"
    await ctx.send(strin)


def resp(search, n):
    if (on_message("next")):
        return 0


@client.command(aliases=["yt", "YT", "Yt", "Youtube", "YouTube"])
async def youtube(ctx, *, search, n=0):

    url, n = get_yt_url(search, n)
    n += 1
    await ctx.send(url)
    msg = await client.wait_for(
        'message', check=lambda message: message.author == ctx.author)
    msg_content = msg.content
    if msg_content == "next":
        url, n = get_yt_url(search, n)
        n += 1
        await ctx.send(url)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if any(word in message.content for word in [" f ", " F "]):
        await message.channel.send("F")
    if message.content.startswith("f "):
        await message.channel.send("F")
    if message.content.startswith("F "):
        await message.channel.send("F")
    if message.content == "f":
        await message.channel.send("F")
    if message.content == "F":
        await message.channel.send("F")


    await client.process_commands(message)


keep_alive()
client.run(token1)
