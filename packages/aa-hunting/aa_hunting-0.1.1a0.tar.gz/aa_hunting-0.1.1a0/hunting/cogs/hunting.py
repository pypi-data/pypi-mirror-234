# import logging

# from aadiscordbot import __branch__, __version__
# from aadiscordbot.app_settings import get_site_url
# from discord.colour import Color
# from discord.commands import SlashCommandGroup
# from discord.embeds import Embed
# from discord.ext import commands

# from django.conf import settings

# logger = logging.getLogger(__name__)


# class Hunting(commands.Cog):
#     """
#     All about me!
#     """

#     def __init__(self, bot):
#         self.bot = bot

#     about_commands = SlashCommandGroup(
#         "hunting", "Hunting Tools", guild_ids=[int(settings.DISCORD_GUILD_ID)])

#     @about_commands.command(name="discordbot", description="About the Discord Bot", guild_ids=[int(settings.DISCORD_GUILD_ID)])
#     async def discordbot(self, ctx):
#         """
#         All about the bot
#         """

#         return await ctx.respond(embed=embed)


# def setup(bot):
#     bot.add_cog(Hunting(bot))
