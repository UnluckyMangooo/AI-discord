import discord
import aiohttp
import json

TOKEN = "x"  # Your selfbot token
AUTHORIZED_USER_IDS = [12345789123123, 12345789123123]  # Add your authorized user IDs
API_URL = "http://localhost:1234/v1/chat/completions"

RELAY_GUILD_ID = x
RELAY_CHANNEL_ID = x

client = discord.Client()
conversation_history = []

async def get_ai_response(user_input):
    conversation_history.append({"role": "user", "content": user_input})
    payload = {
        "model": "YOUR_LLM",
        "messages": conversation_history,
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(API_URL, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    ai_response = data["choices"][0]["message"]["content"].strip()
                    if ai_response:
                        conversation_history.append({"role": "assistant", "content": ai_response})
                        return ai_response
                    else:
                        return "No response from the model."
                else:
                    return f"API Error {response.status}: {await response.text()}"
        except Exception as e:
            return f"Exception occurred: {str(e)}"

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
    if message.author.id not in AUTHORIZED_USER_IDS:
        return

    if not message.content.strip():
        return

    ai_response = await get_ai_response(message.content.strip())
    chunks = [ai_response[i:i + 2000] for i in range(0, len(ai_response), 2000)]
    for chunk in chunks:
        await message.channel.send(chunk)

    await relay_message(message)

client.run(TOKEN)
