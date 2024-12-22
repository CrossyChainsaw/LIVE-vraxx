import discord
import asyncio
from livevraxx.modules.env import env_variable

intents = discord.Intents().all()
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.event
async def on_message(message):
    # Ignore messages from itself to prevent loops
    if message.author == bot.user:
        return

    # Check if the message starts with the command prefix and matches the "live" command
    if message.content.startswith("lv!live"):
        # Split the message into parts to extract the command and arguments
        parts = message.content.split()
        if len(parts) < 2:
            await message.channel.send("Usage: lv!live <streamer_name>")
            return

        streamer_name = parts[1]

        # Find the 'LIVE' category
        live_category = discord.utils.get(message.guild.categories, name="LIVE")

        # If the 'LIVE' category doesn't exist, create it
        if live_category is None:
            live_category = await message.guild.create_category(name="LIVE")
            # Move the 'LIVE' category to the highest position (0)
            await live_category.edit(position=0)
            await message.channel.send("The 'LIVE' category has been created and moved to the highest position!")

        # Check if a channel with the same name already exists in the category
        existing_channel = discord.utils.get(live_category.channels, name=streamer_name)
        if existing_channel:
            await message.channel.send(f"A channel named '{streamer_name}' already exists in the 'LIVE' category.")
            return

        # Create the new channel in the 'LIVE' category
        new_channel = await message.guild.create_text_channel(name=f"🔴{streamer_name}", category=live_category)
        await message.channel.send(f"Channel '{new_channel.mention}' has been created in the 'LIVE' category!")

        # Send a Twitch link in the newly created channel
        await new_channel.send(f"https://www.twitch.tv/{streamer_name}")

        # Wait for 10800 seconds (3 hours)
        await asyncio.sleep(10800)

        # Delete the newly created channel after 7200 seconds
        await new_channel.delete()
        await message.channel.send(f"Channel '{new_channel.name}' has been deleted after 7200 seconds.")

        # Check if there are any other channels in the 'LIVE' category
        if not live_category.channels:
            # If no channels left, delete the 'LIVE' category
            await live_category.delete()
            await message.channel.send("The 'LIVE' category has been deleted as there are no channels left.")

def run_livevraxx():
    bot.run(env_variable("LIVE_VRAXX_BOT_TOKEN"))
