import os
import discord
from discord.ext import commands
from python_aternos import Client, atserver, atwss
from dotenv import load_dotenv

##### Cambiar response de stop, start y reset a funcion status, code blocks para responses, roles para ejecutar, hosting


load_dotenv()

#Configuración del bot
intents = discord.Intents(messages=True, guilds=True, message_content=True)
bot = commands.Bot(command_prefix='#', intents=intents) 

#Credenciales
secret_key = os.environ['discord_bot']
user = os.environ['aternos_user']
pswd = os.environ['aternos_pswd']
channel_id = os.environ['discord_channel']


print("Iniciando bot")

# Creación websocket
aternos = Client.from_credentials(user, pswd)
srv_1 = aternos.list_servers()[0]   # Cambiar numero para websocket de servidor
socket = srv_1.wss()


def sesion(user, password):
    return Client.from_credentials(user, password)

def servidores(credentials):
    return credentials.list_servers()


def selec_server(srv_no):
    srv_name = int(srv_no) - 1
    i = 0
    for srv in servidores(sesion(user=user, password=pswd)):
        if i is srv_name:
            return srv
        i += 1
        
'''@bot.command(name="help", pass_context=True, help="Help of the bot")
async def help(ctx):
    response = "```Comandos:\n servers: Devuelve los servidores disponibles\n status: Devuelve el estado del servidor que se pasa como parámetro\n start: Inicia el servidor pasado como parámetro\n stop: Apaga el servidor que se pasa como parámetro\n restart: Reinicia el servidor que se pasa como parámetro```"
    await ctx.send(response)'''


@bot.command(name="servers", pass_context=True, help="Lists available servers")
async def list_servers(ctx):
    resp = ""
    i = 1
    print("Request: @server_list")
    for srv in servidores(sesion(user=user, password=pswd)):
        resp += ("\n" + str(i) + ": " + srv.subdomain )
        i += 1
    response = f"```Los servidores registrados son:{resp} ```".format(resp)
    await ctx.send(response)


@bot.command(name="status", pass_context=True, help="States the current state of the mentioned server")
@commands.has_role("Jugador")
async def status(ctx,srv_no):
    try:
        srv = selec_server(srv_no)
        print("Request: @status " + srv.subdomain)
        if srv is not None:
            a = srv.subdomain
            b = srv.status
            response = f"```{a} is currently {b}```".format(srv.domain,srv.status)
            await ctx.send(response)
    except IndexError:
        await ctx.send("No existe")


@bot.command(name="start", pass_context=True, help="Starts the mentioned server")
@commands.has_role("Jugador")
async def start(ctx,srv_no):
    # if 0 == int(srv_no) - 1:
    await socket.connect()
    srv = selec_server(srv_no)
    print("Request: @start  " + srv.subdomain)
    a = srv.subdomain
    b = srv.status
    response = ""
    if srv.status == "offline":
        srv.start()
        response = f"```Starting {a}.```"
        await ctx.send(response)
    else:
        await status(ctx,srv_no)
    



@bot.command(name="restart", pass_context=True, help="restartes the mentioned server")
@commands.has_role("Administrador")
async def restart(ctx,srv_no):
 
    srv = selec_server(srv_no)
    print("Request: @restart  " + srv.subdomain)
    a = srv.subdomain
    b = srv.status
    response = ""
    if srv.status != "online":
        srv.restart()
        response = f"```Restarting {a}.```"
        await ctx.send(response)
    else:
        await status(ctx,srv_no)
    
 


@bot.command(name="stop", pass_context=True, help="Stops the server")
@commands.has_role("Administrador")
async def stop(ctx,srv_no):
    srv = selec_server(srv_no)
    print("Request: @stop   " + srv.subdomain)
    a = srv.subdomain
    b = srv.status
    response = ""
    if srv.status == "online":
        srv.stop()
        response = f"```Shutting down {a}.```"
        await ctx.send(response)
    else:
        await status(ctx,srv_no)
    
    

@bot.event  # para eventos
async def on_command_error(ctx, error):
    response = ""
    if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
            await ctx.send("You are not admin")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Command does not exist")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Add the server number Eg:1")
    else:
        print(error)

bot.run(secret_key)
