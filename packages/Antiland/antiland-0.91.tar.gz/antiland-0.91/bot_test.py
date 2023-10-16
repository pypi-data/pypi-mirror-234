import Antiland
import random
import requests
import tempfile
import os
import base64
import json
from random_word import RandomWords
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import asyncio
import num2words
import time

session_token="r:d236a5d9ebb8e9ff35eee1ecb9f2934b"
dialogue="4fkzGJsDs2"
prefix="/"

bot = Antiland.Bot(prefix,dialogue,session_token)

@bot.command("card")
async def card():
    room= await bot.get_dialogue(dialogue,session_token)
    r = RandomWords()
    # Return a single random word
    random_word=r.get_random_word()

    # Fetch a random image (replace this with your own image source)
    response = requests.get("https://source.unsplash.com/random")
    image = Image.open(BytesIO(response.content))

    # async define font size and color
    font_size = 100
    font_color = (0, 0, 0)  # White

    # Load a font
    font = ImageFont.truetype("Bravest.otf", font_size)  # Replace with your font file path

    # Create a drawing object
    draw = ImageDraw.Draw(image)

    # Calculate text size and position
    text_width, text_height = draw.textsize(random_word, font=font)
    image_width, image_height = image.size
    x = (image_width - text_width) // 2  # Centered horizontally
    y = (image_height - text_height) // 2  # Centered vertically

    # Draw the text on the image
    draw.text((x, y), random_word, font=font, fill=font_color)

    # Save or display the resulting image
    output_path = "output.jpg"
    image.save(output_path)
    await room.send_image(output_path,session_token,room.objectId)
    message=f"Anti User, this is your Anti Card for the next 30 min. Please share a story from your life which comes into your mind first when you look at it. Use the word {random_word} in your story."
    await room.send_message(message,session_token,room.objectId)


@bot.command("bettermeme")
async def random_meme():
    room= await bot.get_dialogue(dialogue,session_token)
    # Fetch a random meme from the API
    url = "https://humor-jokes-and-memes.p.rapidapi.com/memes/random"

    querystring = {"keywords":"rocket","number":"3","media-type":"image","keywords-in-image":"false","min-rating":"4"}

    headers = {
        "X-RapidAPI-Key": "b0fc8067b4msh3a50ee815ad5b20p1bdabajsn79c9d434ed40",
        "X-RapidAPI-Host": "humor-jokes-and-memes.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())

    if response.status_code == 200:
        data = response.json()
        meme_url = data['url']
        print(meme_url)
        with requests.get(meme_url) as meme_response:
            meme_response.raise_for_status()
            with open('output.jpg', 'wb') as output_file:
                for chunk in meme_response.iter_content(chunk_size=8192):
                    output_file.write(chunk)

            # Send the downloaded image
            await room.send_image("output.jpg", session_token, dialogue)

@bot.command("antibonus")
async def antibonus():
    room= await bot.get_dialogue(dialogue,session_token)
    amount=random.randint(5000,9999)
    await room.send_message(
                    f"{prefix}antibonus\n\n"
                    f"+ A daily bonus of random ₭{amount} antikarma points has been added to your account!",session_token,room.objectId
                    )

@bot.command("debugger")
async def debug():
    room= await bot.get_dialogue(dialogue,session_token)
    #await room.add_mod("DAwjrFpEyu",session_token,room.objectId)
    await bot.add_contact("a",session_token)



async def main():
    await bot.start(session_token)

if __name__ == "__main__":
    asyncio.run(main())