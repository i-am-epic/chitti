import discord
import os
import requests
import  json
import praw
import random
from http_alive import keep_alive
from discord.ext import commands
import datetime


print("hekkk")

client = commands.Bot(command_prefix='>', description="This is a Helper Bot")
token1 = os.environ['token']
rcid = os.environ['rcid']
rcs = os.environ['rcs']
rusername = os.environ['rusername']
rp = os.environ['rp']


reddit = praw.Reddit(client_id=rcid,client_secret=rcs,username=rusername,password=rp,user_agent="pypraw")

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]["q"] + "  -" + json_data[0]["a"]
  return quote
  
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
async def ping(ctx):
  await ctx.send(f"{client.latency * 1000}ms")

@client.command()
async def clear(ctx,amount=10000):
  await ctx.channel.purge(amount)

@client.command()
async def f(ctx):
  await ctx.channel.send("f")

@client.command()
async def meme(ctx,subrdt= "meme"):
  subreddit = reddit.subreddit(subrdt)
  all_content = []
  top = subreddit.top(limit="50")
  for content in top:
    all_content.append(content)

  random_content = random.choice(all_content)
  title = random_content.title
  url = random_content.url
  em = discord.Embed(title = title)
  em.set_image(url = url)
  await ctx.send(embed = em)

  
@client.event
async def on_message(message):
  
  if message.content.startswith("hello"):
    await message.channel.send("Hello!")

  if message.content.startswith("inspire"):
    await message.channel.send(get_quote())

keep_alive()
client.run(token1)

