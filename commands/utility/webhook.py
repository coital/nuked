import os, discord, datetime, time, aiohttp
from modules import util
from discord.ext import commands

def setup(bot: commands.Bot):
    bot.add_cog(Webhook(bot))
    
class Webhook(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
    @commands.command(aliases=["wh"])
    async def webhook(self, ctx, arg: str = None, webhook: str = None, *, content: str = None):
        await ctx.message.delete()
        if not arg:
            embed = discord.Embed(
                            title="**Webhook Tools**", 
                            description="Tools to interact with Discord Webhooks.",
                            color=util.get_color(), 
                            timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            embed.add_field(name="**Posting Content to a Webhook**", value=f"to post a message to a webhook, use `{self.client.command_prefix}webhook post <webhook> <message>`.", inline=False)
            embed.add_field(name="**Deleting a Webhook**", value=f"to delete a webhook, use `{self.client.command_prefix}webhook delete <webhook>`.", inline=False)
            embed.add_field(name="**Viewing Webhook Information**", value=f"to view information for a webhook, use `{self.client.command_prefix}webhook info <webhook>`.", inline=False)
            await ctx.send(embed=embed, delete_after=25)
        match arg:
            case "post":
                if not webhook or not content:
                    await ctx.send("missing argument `webhook` or `content`", delete_after=15)
                else:
                    async with aiohttp.ClientSession() as session:
                        async with session.post(webhook, json={"content": content}) as response:
                            if response.ok:
                                await ctx.send(f"successfully posted {content} to {webhook}.", delete_after=10)
                            else:
                                await ctx.send(f"unable to post {content} to {webhook}, response code {response.status}.", delete_after=10)
            case "delete":
                async with aiohttp.ClientSession() as session:
                        async with session.delete(webhook) as response:
                            if response.ok:
                                await ctx.send(f"successfully deleted {webhook}.", delete_after=10)
                            else:
                                await ctx.send(f"unable to delete {webhook}, response code {response.status}.", delete_after=10)
            case "info":
                async with aiohttp.ClientSession() as session:
                        async with session.get(webhook) as response:
                            if response.ok:
                                r = await response.json()
                                embed = discord.Embed(title="**Webhook Info**", color=util.get_color(),
                                    description="Webhook Information", timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                                embed.add_field(name="**Name**", value=f"{r['name']}")
                                embed.add_field(name="**Avatar**", value=f"{r['avatar']}")
                                embed.add_field(name="**ID**", value=f"{r['id']}")
                                embed.add_field(name="**Channel ID**", value=f"{r['channel_id']}")
                                embed.add_field(name="**Guild ID**", value=f"{r['guild_id']}")
                                embed.add_field(name="**Token**", value=f"{r['token']}")
                                await ctx.send(embed=embed, delete_after=20)
                            else:
                                await ctx.send(f"webhook {webhook} likely does not exist, response code {response.status}", delete_after=10)
                    
    