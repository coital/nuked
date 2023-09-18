import discord, datetime, asyncio
from discord.ext import commands
from modules import util

async def setup(bot: commands.Bot):
    await bot.add_cog(OnRelationshipAdd(bot))

class OnRelationshipAdd(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
    @commands.Cog.listener()
    async def on_relationship_add(self, friendship: discord.Relationship):
        match friendship.type:
            case discord.RelationshipType.incoming_request:
                util.log(f"Incoming friend request from [bold]{friendship.user.display_name}#{friendship.user.discriminator}[/bold].")
            case discord.RelationshipType.outgoing_request:
                util.log(f"Outgoing friend request to [bold]{friendship.user.display_name}#{friendship.user.discriminator}[/bold].")
            case discord.RelationshipType.friend:
                util.log(f"A new friend was added: [bold]{friendship.user.display_name}#{friendship.user.discriminator}[/bold].")
    