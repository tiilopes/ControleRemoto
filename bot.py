import os
from getpass import getpass
from dotenv import load_dotenv, set_key
import discord
from discord import app_commands
import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET
import re
import asyncio
from suporte import support_command

# Load environment variables from .env
load_dotenv()

# Constants
VLC_URL = "http://localhost:8080/requests/status.xml"
VLC_COMMAND_URL = VLC_URL + "?command="

# Prompt the user for credentials and save them in .env
env_vars = {
    "DISCORD_TOKEN": "coloque sua chave de bot ",
    "VLC_PASSWORD": "coloque sua senha Lua do VLC ",
    "TMDB_API_KEY": "coloque sua TMDB API: key "
}

env_file = '.env'
for var, prompt in env_vars.items():
    if not os.getenv(var):
        value = getpass(prompt) if "PASSWORD" in var else input(prompt)
        with open(env_file, 'a') as f:
            set_key(env_file, var, value)

# Retrieve the values after possibly setting them
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
VLC_PASSWORD = os.getenv("VLC_PASSWORD")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
VERSION = "1.0.0.1"

class PlexcordClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f"✅ Bot 'Controle Remoto' conectado. Versão: {VERSION}. Comandos sincronizados.")
        await self.tree.sync()

client = PlexcordClient()

class VLCView(discord.ui.View):
    @discord.ui.button(label="▶️", style=discord.ButtonStyle.green)
    async def play_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        ok, msg = send_vlc_command("pl_play")
        await interaction.response.send_message("▶️ " + msg if ok else "❌ " + msg, ephemeral=True, delete_after=10)

    @discord.ui.button(label="⏯️", style=discord.ButtonStyle.grey)
    async def pause_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        ok, msg = send_vlc_command("pl_pause")
        await interaction.response.send_message("⏸️ " + msg if ok else "❌ " + msg, ephemeral=True, delete_after=10)

    @discord.ui.button(label="⏹️", style=discord.ButtonStyle.red)
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        ok, msg = send_vlc_command("pl_stop")
        await interaction.response.send_message("⏹️ " + msg if ok else "❌ " + msg, ephemeral=True, delete_after=10)

    @discord.ui.button(label="Status", style=discord.ButtonStyle.blurple)
    async def status_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        data, err = get_vlc_status()
        if err:
            message = await interaction.followup.send(f"❌ Erro: {err}", ephemeral=True)
            await asyncio.sleep(60)
            await message.delete()
            return

        movie_info = get_movie_info_from_tmdb(data['title'])
        if movie_info:
            tmdb_title = movie_info.get('title', data['title'])
            sinopse = movie_info.get('plot', "Sinopse não disponível.")
            poster = movie_info.get('poster', "")
            rating = movie_info.get('rating', "N/A")
        else:
            tmdb_title = data['title']
            sinopse = "Sinopse não disponível."
            poster = ""
            rating = "N/A"

        time_remaining = data['length'] - data['time']

        embed = discord.Embed(title=f"Título: {tmdb_title}", description=f"Sinopse: {sinopse}", color=discord.Color.blue())
        if poster:
            embed.set_image(url=poster)
        embed.add_field(name="Avaliação", value=rating, inline=True)
        embed.add_field(name="Arquivo", value=data['filename'], inline=False)
        embed.add_field(name="Estado", value=data['state'], inline=True)
        embed.add_field(name="Tempo decorrido", value=fmt_time(data['time']), inline=True)
        embed.add_field(name="Tempo restante", value=fmt_time(time_remaining), inline=True)

        message = await interaction.followup.send(embed=embed, ephemeral=True)
        await asyncio.sleep(60)
        await message.delete()

class SupportView(discord.ui.View):
    @discord.ui.button(label="❓ Suporte", style=discord.ButtonStyle.green)
    async def support_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await support_command(interaction)

@client.tree.command(name="controle", description="Exibe os controles do VLC e suporte")
async def control(interaction: discord.Interaction):
    view = VLCView()
    view.add_item(SupportView().children[0])  # Adiciona o botão de suporte à view
    await interaction.response.send_message("Controle do VLC:", view=view)

def send_vlc_command(command):
    url = VLC_COMMAND_URL + command
    try:
        response = requests.get(url, auth=HTTPBasicAuth('', VLC_PASSWORD), timeout=5)
        response.raise_for_status()
        return True, "Comando enviado com sucesso."
    except requests.exceptions.HTTPError as e:
        return False, f"Erro HTTP {response.status_code}: {e}"
    except Exception as err:
        return False, str(err)

def fetch_vlc_data():
    try:
        response = requests.get(VLC_URL, auth=HTTPBasicAuth('', VLC_PASSWORD), timeout=5)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return None

def parse_xml_field(root, field):
    return root.findtext(field, 'Desconhecido')

def parse_info_field(root, name):
    for info in root.findall(".//category[@name='meta']/info"):
        if info.get('name') == name:
            return info.text or "Desconhecido"
    return "Desconhecido"

def get_vlc_status():
    xml = fetch_vlc_data()
    if xml is None:
        return None, "Erro ao buscar dados VLC"

    root = ET.fromstring(xml)
    state = parse_xml_field(root, "state")
    time = int(parse_xml_field(root, "time"))
    length = int(parse_xml_field(root, "length"))
    
    title = parse_info_field(root, "title")
    filename = parse_info_field(root, "filename")

    if title == "Desconhecido":
        title = format_title_from_filename(filename)

    return {
        "state": state,
        "time": time,
        "length": length,
        "title": title,
        "filename": filename
    }, None

def format_title_from_filename(filename):
    title = os.path.splitext(filename)[0]
    title = re.sub(r'[._]', ' ', title)
    title = re.split(r'\b(\d{4})\b', title)[0]
    return re.sub(r'\s+', ' ', title).strip()

def get_movie_info_from_tmdb(title):
    url = f"https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": title,
        "language": "pt-BR"
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            movie = data['results'][0]
            return {
                "title": movie.get("title", "Título não encontrado"),
                "plot": movie.get("overview", "Sinopse não disponível."),
                "poster": f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}",
                "rating": movie.get("vote_average", "N/A")
            }
    return None

def fmt_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{h:02}:{m:02}:{s:02}"

client.run(DISCORD_TOKEN)