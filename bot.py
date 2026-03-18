import discord
import subprocess
import os

TOKEN = os.getenv("")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot conectado como {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith(".dump"):
        if not message.attachments:
            await message.channel.send("Debes enviar un archivo `.lua` junto con `.dump`.")
            return

        attachment = message.attachments[0]

        if not attachment.filename.endswith(".lua"):
            await message.channel.send("Solo acepto archivos `.lua`.")
            return

        file_path = attachment.filename
        await attachment.save(file_path)

        await message.channel.send("Procesando archivo…")

        result = subprocess.run(
            ["python", "controller_main.py", file_path, "--mode=full", "--output=analysis.json"],
            capture_output=True,
            text=True
        )

        preview = result.stdout[-1800:] if result.stdout else "Sin salida."

        if os.path.exists("analysis.json"):
            await message.channel.send(
                "Aquí está el dump:",
                file=discord.File("analysis.json")
            )

        await message.channel.send(f"```{preview}```")

client.run(TOKEN)