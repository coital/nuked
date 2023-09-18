import discord, datetime, time, os
from discord.ext import commands
from modules import util

async def setup(bot: commands.Bot):
    await bot.add_cog(Backup(bot))

class Backup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
    @commands.command()
    async def backup(self, ctx, option: str=None):
        embed = discord.Embed(
                                title=f"**Backup**", color=util.get_color(), 
                                description=f"Backup your friends, servers, or both.", 
                                timestamp=datetime.datetime.utcfromtimestamp(time.time()))
        embed.add_field(name="**Backing up Friends**", value=f"to backup friends, use `{self.client.command_prefix}backup friends`.", inline=False)
        embed.add_field(name="**Backing up Servers**", value=f"to backup servers, use `{self.client.command_prefix}backup servers`.", inline=False)
        embed.add_field(name="**Complete Backup**", value=f"to backup everything, use `{self.client.command_prefix}backup all`.", inline=False)
        await ctx.message.delete()
        if not option:
            await ctx.send(util.embed_to_str(embed), delete_after=20)
        else:
            match option.lower():
                case "friends":
                    if not os.path.isdir("./backups/"):
                        os.mkdir("backups")
                    with open("friend-backup.txt", "a", encoding="utf-8") as f:
                        f.write(f"Backup for user {self.client.user.display_name}#{self.client.user.discriminator}\nFriend Count: {len(self.client.user.friends)}\nServer Count: {len(self.client.guilds)}\nBackup Date: {datetime.datetime.now().strftime('%m/%d/%Y, %H:%M:%S %p')}\n")
                        for friend in self.client.user.friends:
                            f.write(f"\nFriend:\n{friend.name}#{friend.discriminator}\nID:\n{friend.id}\n")
                            util.log(f"Backed up friend: {friend.name}#{friend.discriminator}")
                case "servers":
                    if not os.path.isdir("./backups/"):
                        os.mkdir("backups")
                    with open("backups/server-backup.txt", "a", encoding="utf-8") as f:
                        f.write(f"Backup for user {self.client.user.display_name}#{self.client.user.discriminator}\nFriend Count: {len(self.client.user.friends)}\nServer Count: {len(self.client.guilds)}\nBackup Date: {datetime.datetime.now().strftime('%m/%d/%Y, %H:%M:%S %p')}\n")
                        for guild in self.client.guilds:
                            f.write(f'\nServer:\n{guild.name}\nID:\n{guild.id}\nOwner ID: {guild.owner_id}\n')
                            util.log(f"Backed up guild: {guild.name}")
                case "all":
                    if not os.path.isdir("./backups/"):
                        os.mkdir("backups")
                    with open("backups/full-backup.txt", "a", encoding="utf-8") as f:
                        f.write(f"Backup for user {self.client.user.display_name}#{self.client.user.discriminator}\nFriend Count: {len(self.client.user.friends)}\nServer Count: {len(self.client.guilds)}\nBackup Date: {datetime.datetime.now().strftime('%m/%d/%Y, %H:%M:%S %p')}\n")
                        for friend in self.client.user.friends:
                            f.write(f"\nFriend:\n{friend.name}#{friend.discriminator}\nID:\n{friend.id}\n")
                            util.log(f"Backed up friend: {friend.name}#{friend.discriminator}")
                        for guild in self.client.guilds:
                            f.write(f'\nServer:\n{guild.name}\nID:\n{guild.id}\nOwner ID: {guild.owner_id}\n')
                            util.log(f"Backed up guild: {guild.name}")
                case _:
                    await ctx.send(embed=embed, delete_after=20)