import discord, os, time
from discord import app_commands, Intents, ui, Interaction
from discord.colour import Color
from dotenv import load_dotenv
from dotez import load_ez, get_item

load_ez()  # Load the .ez file into the dotez package
load_dotenv()  # Access the .env file
TOKEN = os.getenv('TOKEN')  # Get the TOKEN variable from the .env file


class Client(discord.Client):
    def __init__(self):
        super().__init__(intents=Intents.default())
        self.synced = False  # So the bot doesn't sync commands more than once

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:  # Check if commands have been synced
            await tree.sync(guild=discord.Object(id=get_item("GUILD_ID")))  # Guild specific, leave blank if global
            # (global registration can take up to a day)
            self.synced = True

        tree.clear_commands(guild=discord.Object(id=get_item("GUILD_ID")))  # Clear all commands from the previous
        # command tree to avoid issues
        print(f"Successfully cleared commands.")
        tree.add_command(command_list)
        tree.add_command(suggestion)
        print(f"Successfully added commands.")


class SuggestionModal(ui.Modal, title="Submit a Suggestion"):
    suggestion = ui.TextInput(
        label="What's your suggestion?",
        style=discord.TextStyle.paragraph,
        placeholder="Suggestion",
        required=True,
        max_length=2000
    )

    async def on_submit(self, interaction: Interaction):
        # Send an embed with the suggestion response to a suggestion channel
        embed = discord.Embed(
            title=f"Suggestion submitted by {interaction.user.display_name}",
            description=f"<t:{int(time.time())}>",
            color=Color.from_rgb(47, 49, 54)
        )
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        embed.add_field(name="Suggestion", value=self.suggestion)

        channel = client.get_channel(get_item("SUGGESTIONS_CHANNEL"))
        await channel.send(embed=embed)  # Send the embed

        # Respond to user saying suggestion was submitted
        embed = discord.Embed(
            title=f"Suggestion submitted by {interaction.user.display_name}",
            description=f"<t:{int(time.time())}>",
            color=Color.from_rgb(47, 49, 54)
        )
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        embed.add_field(name="Suggestion", value=self.suggestion)

        await interaction.response.send_message("Suggestion Submitted", ephemeral=True)


# Initializing the client and command tree
client = Client()
tree = app_commands.CommandTree(client)


"""
The following commands are Official Commands
"""


@tree.command(
    guild=discord.Object(id=get_item("GUILD_ID")),
    name='suggestion',
    description='Submit a suggestion to the staff team!',
)
async def suggestion(interaction: discord.Interaction):
    await interaction.response.send_modal(SuggestionModal())


"""
The following commands are Test Commands
"""


# Fetch all the commands that exist in the bot's code
@tree.command(
    guild=discord.Object(id=get_item("GUILD_ID")),
    name='command-list',
    description='This is a developer intended command, but feel free to try it out.',
)
async def command_list(interaction: discord.Interaction):
    fetched = await tree.fetch_commands(
        guild=discord.Object(id=get_item("GUILD_ID")))  # Fetch all the commands registered with the command tree
    await interaction.response.send_message(fetched, ephemeral=True)


client.run(TOKEN)  # Connect to the bot using Discord.api
