import re
import requests
from json import loads
from os import environ
from discord import Intents
from discord.ext import commands
from bs4 import BeautifulSoup as soup

bot = commands.Bot(command_prefix="~",intents=Intents.all())

@bot.command()
async def ac(ctx,u = None):
	if not u:
		u = loads(environ["username"])[ctx.author.name]
	s = soup(requests.get(f"https://judge.hkoi.org/user/{u}",cookies=loads(environ["cookies"])).content,"html.parser")
	y = ["23","22","21","19","18","17","16"]
	a,c = [[i]+[0]*12 for i in y],0
	for i in s.find("div",class_='profile-solved').find_all():
		if re.match("^PL\d{2}[A-L]$",s:=i.text):
			a[y.index(s[2:4])][ord(s[4])-64] = {"a":"[0;32m✓[0m","b":"[0;31m⨯[0m","c":" "}[i.get("class")[0]]
			if "a" in i.get("class"):
				c += 1
	await ctx.send("```ansi\nuser: %s   solved: %s\n\n   A B C D E F G H I J K L\n%s```"%(u,c,"\n".join(" ".join(i) for i in a)))
	
bot.run(environ["token"])