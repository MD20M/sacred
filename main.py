import requests
import os
import json
import asyncio
import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ui import Button, View
from nextcord.ext import commands, tasks
import schedule
import datetime
import time
import pytz
from flask import Flask
from threading import Thread
from keep_alive import keep_alive

intents = nextcord.Intents.default()
intents.message_content = True



stats = requests.get("https://pro-api.solscan.io/v1.0/public/nft/statistic/overview")

total_holders = stats.json()['data']['total_holders']

total_nfts = stats.json()['data']['total_nfts']

total_collections = stats.json()['data']['total_collections']

total_listing = stats.json()['data']['total_nft_listing']

active_users = stats.json()['data']['user_active_24']

volume_24 = stats.json()['data']['volume_24']

statistics = {'total_nfts':total_nfts, 'total_listing':total_listing, 'active_users':active_users}

def update_statistics():
  stats = requests.get("https://pro-api.solscan.io/v1.0/public/nft/statistic/overview")
  total_holders = stats.json()['data']['total_holders']
  total_nfts = stats.json()['data']['total_nfts']
  total_collections = stats.json()['data']['total_collections']
  total_listing = stats.json()['data']['total_nft_listing']
  active_users = stats.json()['data']['user_active_24']
  volume_24 = stats.json()['data']['volume_24']
  statistics = {'total_nfts':total_nfts, 'total_listing':total_listing, 'active_users':active_users}
  

activity=nextcord.Activity(type=nextcord.ActivityType.watching, name=f"\nTotal Live Solana Assets: {statistics['total_nfts']}\nTotal Secondary Listings: {statistics['total_listing']}\nTotal Active NFT Wallets: {statistics['active_users']}")


bot = commands.Bot(command_prefix='!', intents=intents, activity=activity)


@bot.event
async def on_ready():
    print('\nBot is online\n')
    print(bot.user.name+'\n')
    print(bot.user.id)
    print('\nstarted')
    i = 0
    while True:
     eastern = pytz.timezone('Europe/London')
     now = datetime.datetime.now(eastern)
     if now.hour == 14 and now.minute == 40: 
        await get_stats()
        i=0
        time.sleep(60)
     else:
        if (i%20==0):

         update_statistics()
         await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name=f"\nTotal Live Solana Assets: {statistics['total_nfts']}\nTotal Secondary Listings: {statistics['total_listing']}\nTotal Active NFT Wallets: {statistics['active_users']}"))
        channel2 = bot.get_channel(1084080567135514664)
        await channel2.send("Running!")
        i = i + 1
        time.sleep(58)



    

async def get_stats():
  channel = bot.get_channel(801440380691677258)
  stats = requests.get("https://pro-api.solscan.io/v1.0/public/nft/statistic/overview")
  total_holders = stats.json()['data']['total_holders']
  total_nfts = stats.json()['data']['total_nfts']
  total_collections = stats.json()['data']['total_collections']
  total_listing = stats.json()['data']['total_nft_listing']
  active_users = stats.json()['data']['user_active_24']
  volume_24 = stats.json()['data']['volume_24']
  await channel.send(f"Total NFTs on Solana ATM: {total_nfts}\nTotal Secondary Listings: {total_listing}\nTotal Active NFT Wallets: {active_users}")


keep_alive()
token = os.environ['Token']
bot.run(token)
