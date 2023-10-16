import Antiland
import asyncio

session_token = ""
dialogue = ""
prefix = "!"

bot = Antiland.Bot(prefix, dialogue, session_token)

@bot.command("hello")
async def say_hello():
    room = await bot.get_dialogue(dialogue, session_token)
    await room.send_message("hello world", session_token, dialogue)

@bot.command("debug")
async def debug():
    room =await bot.get_dialogue("enter dialogue id here", session_token)
    await room.send_message("BOT IS WORKING", session_token, dialogue)

async def main():
    await bot.start(session_token)

if __name__ == "__main__":
    asyncio.run(main())
