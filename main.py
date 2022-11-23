import discord
from discord import app_commands, Intents, ui, Interaction
from discord.colour import Color
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()  # Access the .env file
TOKEN = os.getenv('TOKEN')  # Get the TOKEN variable from the .env file

guild_id = 847962669797474334


class Client(discord.Client):
    def __init__(self):
        super().__init__(intents=Intents.default())
        self.synced = False  # So the bot doesn't sync commands more than once

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:  # Check if commands have been synced
            await tree.sync(guild=discord.Object(id=guild_id))  # Guild specific, leave blank if global (global
            # registration can take up to a day)
            self.synced = True

        tree.clear_commands(guild=discord.Object(id=guild_id))  # Clear all commands from the previous command tree
        # to avoid issues
        print(f"Successfully cleared commands.")
        tree.add_command(command_list)
        print(f"Successfully added commands.")


# Initializing the client and command tree
client = Client()
tree = app_commands.CommandTree(client)


"""
The follow commands are Test Commands
"""


# Fetch all the commands that exist in the bot's code
@tree.command(
    guild=discord.Object(id=guild_id),
    name='command-list',
    description='This is a developer intended command, but feel free to try it out.',
)
async def command_list(interaction: discord.Interaction):
    fetched = await tree.fetch_commands(
        guild=discord.Object(id=guild_id))  # Fetch all the commands registered with the command tree
    await interaction.response.send_message(fetched, ephemeral=True)


client.run(TOKEN)  # Connect to the bot using Discord.api
