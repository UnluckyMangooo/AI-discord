#pip uninstall discord.py
#pip install git+https://github.com/dolfies/discord.py-self
#reverse when done

import discord
import aiohttp
import json
import re

TOKEN = "x"  
AUTHORIZED_USER_IDS = [123456789123, 123456789123] #Only authorized users can interact with AI
API_URL = "http://localhost:1234/v1/chat/completions"

RELAY_GUILD_ID = x #put relay (to store messages) server ID here
RELAY_CHANNEL_ID = x #put relay (to store messages) channel ID here

PREFIXES = ["!", "AI", "ai", "god answer me"]

client = discord.Client()
conversation_history = []

# AI response handler with <think> filtering
async def get_ai_response(user_input):
    conversation_history.append({"role": "user", "content": user_input})
    payload = {
        "model": "dolphin-2.8-experiment26-7b",
        "messages": conversation_history,
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(API_URL, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    ai_response = data["choices"][0]["message"]["content"].strip()

                    # Remove <think>...</think> blocks
                    ai_response = re.sub(r"<think>.*?</think>", "", ai_response, flags=re.DOTALL).strip()

                    if ai_response:
                        conversation_history.append({"role": "assistant", "content": ai_response})
                        return ai_response
                    else:
                        return "No response from the model."
                else:
                    return f"API Error {response.status}: {await response.text()}"
        except Exception as e:
            return f"Exception occurred: {str(e)}"

# Optional: relay messages to a fixed channel
async def relay_message(message):
    relay_guild = client.get_guild(RELAY_GUILD_ID)
    if not relay_guild:
        return
    relay_channel = relay_guild.get_channel(RELAY_CHANNEL_ID)
    if not relay_channel:
        return

    embed = discord.Embed(
        title="Relayed Message",
        description=f"**From:** {message.author} in {message.channel.mention}\n\n**Message:**\n{message.content}",
        color=discord.Color.blurple()   
    )
    await relay_channel.send(embed=embed)

@client.event
async def on_ready():
    print(f"Logged in as {client.user} (selfbot)")
    print(f"Authorized users: {AUTHORIZED_USER_IDS}")

@client.event
async def on_message(message):
    # Only respond to authorized users
    if message.author.id not in AUTHORIZED_USER_IDS:
        return

    # Check for prefix trigger
    if any(message.content.startswith(prefix) for prefix in PREFIXES):
        prefix_used = next(prefix for prefix in PREFIXES if message.content.startswith(prefix))
        user_input = message.content[len(prefix_used):].strip()
        if not user_input:
            return

        ai_response = await get_ai_response(user_input)
        chunks = [ai_response[i:i + 2000] for i in range(0, len(ai_response), 2000)]
        for chunk in chunks:
            await message.channel.send(chunk)

        await relay_message(message)

# Run client
client.run(TOKEN)
