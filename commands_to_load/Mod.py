from discord.ext import commands
import discord
import asyncio
import json
import datetime
from helper_files.embed import embed as em
import helper_files.settings as settings

import logging
logger = logging.getLogger('wall_e')

class Mod():

    async def rekt(self, ctx):
        logger.info('[Mod rekt()] sending troll to unauthorized user')
        lol = '[secret](https://www.youtube.com/watch?v=dQw4w9WgXcQ)'
        eObj = await em(ctx, title='Minion Things', author=settings.BOT_NAME, avatar=settings.BOT_AVATAR, description=lol)        
        if eObj is not False:
            msg = await ctx.send(embed=eObj)
            await asyncio.sleep(5)
            await msg.delete()
            logger.info('[Mod rekt()] troll message deleted')
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=['em'])
    async def embed(self, ctx, *arg):
        logger.info('[Mod embed()] embed function detected by user ' + str(ctx.message.author))
        await ctx.message.delete()
        logger.info('[Mod embed()] invoking message deleted')

        if not arg:
            logger.info("[Mod embed()] no args, so command ended")
            return
        
        if not ctx.message.author in discord.utils.get(ctx.guild.roles, name="Minions").members:
            logger.info('[Mod embed()] unathorized command attempt detected. Being handled.')
            await self.rekt(ctx)
            return
        
        logger.info('[Mod embed()] minion confirmed')
        fields = []
        desc = ''
        arg = list(arg)
        argLen = len(arg)
        # odd number of args means description plus fields
        if not argLen%2 == 0:
            desc = arg[0]
            arg.pop(0)
            argLen = len(arg)
            
        i = 0
        while i < argLen:
            fields.append([arg[i], arg[i+1]])
            i +=2

        name = ctx.author.nick or ctx.author.name
        eObj = await em(ctx, description=desc, author=name, avatar=ctx.author.avatar_url, colour=0xffc61d ,content=fields)
        if eObj is not False:
            await ctx.send(embed=eObj)

    @commands.command(aliases=['warn'])
    async def modspeak(self, ctx, *arg):
        logger.info('[Mod modspeak()] modspeack function detected by minion ' + str(ctx.message.author))
        await ctx.message.delete()
        logger.info('[Mod modspeak()] invoking message deleted')

        if not arg:
            logger.info("[Mod modspeak()] no args, so command ended")
            return

        if not ctx.message.author in discord.utils.get(ctx.guild.roles, name="Minions").members:
            logger.info('[Mod modspeak()] unathorized command attempt detected. Being handled.')
            await self.rekt(ctx)
            return

        msg = ''
        for wrd in arg:
            msg += wrd + ' '

        eObj = await em(ctx, title='ATTENTION:', colour=0xff0000, author=ctx.author.display_name, avatar=ctx.author.avatar_url, description=msg, footer='Moderator Warning')
        if eObj is not False:
            await ctx.send(embed=eObj)
    
    async def on_raw_message_delete(self, payload):
        logger.info('[Mod on_raw_message_delete()] message deletion detected.')
        channel = self.bot.get_channel(settings.deleted_channel_id)
        time_deleted = str(datetime.datetime.now())
        deleted_message = payload.cached_message
        if deleted_message == None:
            embed = discord.Embed(title="Message Deleted", description=time_deleted, color=0x000000)
            embed.add_field(name="Author", value="Not Cached", inline=False)
            embed.add_field(name="Channel", value=self.bot.get_channel(payload.channel_id), inline=False)
            embed.add_field(name="Content", value="Not Cached", inline=False)
            await channel.send(embed=embed)
        else:
            embed = discord.Embed(title="Message Deleted", description=time_deleted, color=0x000000)
            embed.add_field(name="Author", value=deleted_message.author, inline=False)
            embed.add_field(name="Channel", value=deleted_message.channel, inline=False)
            embed.add_field(name="Content", value=deleted_message.content, inline=False)
            await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Mod(bot))
