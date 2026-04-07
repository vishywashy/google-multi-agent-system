import discord
from discord.ext import commands
from ScenarioThingy import Runner
from dotenv import load_dotenv
import os
# 1. Setup Intents

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True  # Allows bot to read what people type

# 2. Define the Bot and its prefix (e.g., !hello)
bot = commands.Bot(command_prefix='!', intents=intents, strip_after_prefix=True)

@bot.event
async def on_ready():
    print(f'Bot is online as {bot.user}')

# 3. Create a simple command
@bot.command()
async def TaskForce(ctx, *, question):
    if ctx.message.reference:
        replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        original_text = replied_message.content
        response = await Runner(prompt = original_text+question)
        await ctx.send(response)
    # This responds directly to the channel where !test was typed
    response = await Runner(question)
    await ctx.send(response)

@bot.command()
async def Uses(ctx):
    await ctx.send("""Task Force
is a coordinated multi-agent system designed to act as a high-level administrative squad for your team. It bridges the gap between your Discord conversations and your professional workspace by managing Gmail and Google Calendar as an integrated unit.
Here is how the Task Force operates:
📧 The Communications Wing (Gmail)
The bot acts as a dedicated intelligence officer for your inbox. It can read incoming mail to provide instant sitreps on important messages directly in Discord, ensuring you never miss a priority update. When a response is needed, it can write and dispatch professional emails on your behalf, allowing you to handle external correspondence without ever leaving the chat.
📅 The Logistics Wing (Google Calendar)
To keep your schedule tight, the Task Force takes full tactical command of your calendar:

    Deployment: It can write new events, meetings, or mission-critical reminders to your schedule instantly.
    Intelligence: It reads your upcoming agenda to provide "Daily Briefs," ensuring the whole team knows exactly what the mission parameters are for the day.
    Strategic Cleanup: If plans change, the bot can delete specific events or "wipe" an entire afternoon block to clear space for emergency deep-work sessions.

🤖 The Multi-Agent Advantage
Unlike a standard bot, Task Force uses multiple agents that talk to each other. For example, if one agent reads an email requesting a meeting, it can automatically signal another agent to write that event into your calendar and a third to send a confirmation email. It turns manual, multi-step admin work into a single, fluid team operation.
To initialize your squad and see the agents in action, simply use !Taskforce.""")

       

bot.run(os.environ.get("DiscordBot"))