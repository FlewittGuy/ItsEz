import discord
from discord import app_commands, Intents, ui, Interaction
from discord.colour import Color
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()  # Access the .env file
TOKEN = os.getenv('TOKEN')  # Get the TOKEN variable from the .env file

guild_id = 847962669797474334


class client(discord.Client):
    def __init__(self):
        super().__init__(intents=Intents.default())
        self.synced = False  # So the bot doesn't sync commands more than once

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:  # Check if commands have been synced
            await tree.sync(guild = discord.Object(id=guild_id))  # Guild specific, leave blank if global (global registration can take up to a day)
            self.synced = True

        tree.clear_commands(guild = discord.Object(id=guild_id))  # Clear all commands from the previous command tree to avoid issues
        print(f"Successfully cleared commands.")
        tree.add_command(command_list)
        tree.add_command(test_modal)
        print(f"Successfully added commands.")


"""
Initializing the modals that will be used later in the commands
"""


class mrz_modal(ui.Modal, title = "Test Modal"):
    answer = ui.TextInput(
        label="Is MrZ cool?",
        style=discord.TextStyle.short,
        placeholder="Answer", required=True,
        max_length=3
    )
    confirmation = ui.TextInput(label="Are you sure?",
        style=discord.TextStyle.short,
        placeholder="Answer", required=True,
        max_length=3
    )

    async def on_submit(self, interaction: Interaction):
        embed = discord.Embed(title=self.title, timestamp=datetime.now(), color=Color.from_rgb(47,49,54))
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        embed.add_field(name=self.answer.label, value=self.answer, inline=False)
        embed.add_field(name=self.confirmation.label, value=self.confirmation, inline=False)
        await interaction.response.send_message(embed=embed)


# Initializing the client and command tree
client = client()
tree = app_commands.CommandTree(client)


"""
The follow commands are Test Commands
"""


# Fetch all the commands that exist in the bot's code
@tree.command(
    guild = discord.Object(id=guild_id), 
    name = 'command-list', 
    description='This is a developer intended command, but feel free to try it out.',
)
async def command_list(interaction: discord.Interaction):
    fetched = await tree.fetch_commands(guild = discord.Object(id=guild_id))  # Fetch all the commands registered with the command tree
    await interaction.response.send_message(fetched, ephemeral = True)


# Generate a modal that asks the user if MrZ is a cool person (they are)
@tree.command(
    guild = discord.Object(id=guild_id), 
    name = 'test-modal', 
    description='Discord modal test.',
)
async def test_modal(interaction: discord.Interaction):
    await interaction.response.send_modal(mrz_modal())


client.run(TOKEN)