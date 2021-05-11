import discord
import os
import requests
import  json
import praw
import random
from http_alive import keep_alive
from discord.ext import commands
import time


print("hekkk")

client = commands.Bot(command_prefix='ch ', description="This is a Helper Bot")
token1 = os.environ['token']
rcid = os.environ['rcid']
rcs = os.environ['rcs']
rusername = os.environ['rusername']
rp = os.environ['rp']


reddit = praw.Reddit(client_id=rcid,client_secret=rcs,username=rusername,password=rp,user_agent="pypraw",check_for_async=False)

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
  elif age>21:
    age += random.randint(-15, 10)

  return age


def get_gender(name):
  response = requests.get(f"https://api.genderize.io/?name={name}")
  json_data = json.loads(response.text)
  gender= str(json_data["gender"])+" of "+str((json_data["probability"]*100)//1)+"%."
  return gender

def get_country(name):
  response = requests.get(f"https://api.nationalize.io/?name={name}")
  json_data = json.loads(response.text)
  country= str(json_data["country"])
  country = list(eval(country))

  country1 = country[0]["country_id"]+" of "+str((country[0]["probability"]*100)//1)+"%.\n"+country[1]["country_id"]+" of "+str((country[1]["probability"]*100)//1)+"%.\n"+country[2]["country_id"]+" of "+str((country[2]["probability"]*100)//1)+"%.\n"
  
  return country1

@client.event
async def on_ready():
  print("Bots up and running as {0.user}".format(client))

@client.event
async def on_member_join(member):
  print(f"Welcome {member} to the server")
  await message.channel.send(f"Welcome {member} to the server")


@client.event
async def on_member_remove(member):
  print(f"{member} left us")
  await message.channel.send(f"{member} left us")

@client.command()
async def age(ctx,member):
  await ctx.channel.send(get_age_name(member))
  
@client.command()
async def gender(ctx,member):
  await ctx.channel.send(get_gender(member))

@client.command()
async def country(ctx,member):
  await ctx.channel.send(get_country(member))

@client.command()
async def clear(ctx,amount=10):
  await ctx.channel.send("Make sure bot has message moderation permission, if not add a role with the permisiion")
  await ctx.channel.purge(limit = amount+2)

@client.command()
async def f(ctx):
  await ctx.channel.send("f")

@client.command()
async def meme(ctx,subrdt= "meme"):
  subreddit = reddit.subreddit(subrdt)
  all_content = []
  top = subreddit.top(limit=50)
  for content in top:
    all_content.append(content)

  random_content = random.choice(all_content)
  title = random_content.title
  url = random_content.url
  em = discord.Embed(title = title)
  em.set_image(url = url)
  await ctx.send(embed = em)

@client.command()
async def rstart(ctx,subrdt= "meme",times = 1 ,slow = 30):
  subreddit = reddit.subreddit(subrdt)
  all_content = []
  top = subreddit.top(limit=times*10)
  i=1
  for content in top:
    await ctx.send(f"Hold on finding best of the best......{i//10}/{times}")
    all_content.append(content)
    i=i+1
  await ctx.channel.purge(limit = 1)

  for i in range(times):
    random_content = random.choice(all_content)
    title = random_content.title
    url = random_content.url
    em = discord.Embed(title = title)
    em.set_image(url = url)
    await ctx.send(embed = em)
    time.sleep(slow)
   
@client.command()
async def ping(ctx):
  await ctx.send(f"{client.latency * 1000}ms")

@client.command()
async def inspire(ctx):
  await ctx.send(get_quote())
  

keep_alive()
client.run(token1)

