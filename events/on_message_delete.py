import discord, datetime, asyncio
from discord.ext import commands
from modules import util

async def setup(bot: commands.Bot):
    await bot.add_cog(OnMessageDelete(bot))

class OnMessageDelete(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.id == self.client.user.id:
            return
        if self.client.msgsniper:
            if isinstance(message.channel, discord.DMChannel):
                if message.author.bot:
                    return
                attachments = message.attachments
                if len(attachments) == 0:
                    message_content = "`" + str(discord.utils.escape_markdown(str(message.author))) + "`: " + str(
                        message.content).replace("@everyone", "@\u200beveryone").replace("@here", "@\u200bhere")
                    await message.channel.send(message_content)
                else:
                    links = ""
                    for attachment in attachments:
                        links += attachment.proxy_url + "\n"
                    message_content = "`" + str(
                        discord.utils.escape_markdown(str(message.author))) + "`: " + discord.utils.escape_mentions(
                        message.content) + "\n\n**Attachments:**\n" + links
                    await message.channel.send(message_content)
        if len(self.client.sniped_message_dict) > 250:
            self.client.sniped_message_dict.clear()
        if len(self.client.snipe_history_dict) > 250:
            self.client.snipe_history_dict.clear()
        attachments = message.attachments
        if len(attachments) == 0:
            channel_id = message.channel.id
            message_content = "`" + str(discord.utils.escape_markdown(str(message.author))) + "`: " + str(
                message.content).replace("@everyone", "@\u200beveryone").replace("@here", "@\u200bhere")
            self.client.sniped_message_dict.update({channel_id: message_content})
            if channel_id in self.client.snipe_history_dict:
                pre = self.client.snipe_history_dict[channel_id]
                post = str(message.author) + ": " + str(message.content).replace(
                    "@everyone", "@\u200beveryone").replace("@here", "@\u200bhere")
                self.client.snipe_history_dict.update(
                    {channel_id: pre[:-3] + post + "\n```"})
            else:
                post = str(message.author) + ": " + str(message.content).replace(
                    "@everyone", "@\u200beveryone").replace("@here", "@\u200bhere")
                self.client.snipe_history_dict.update(
                    {channel_id: "```\n" + post + "\n```"})
        else:
            links = ""
            for attachment in attachments:
                links += attachment.proxy_url + "\n"
            channel_id = message.channel.id
            message_content = "`" + str(discord.utils.escape_markdown(str(message.author))) + "`: " + \
                discord.utils.escape_mentions(
                    message.content) + "\n\n**Attachments:**\n" + links
            self.client.sniped_message_dict.update({channel_id: message_content})
    