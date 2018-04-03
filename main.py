import discord
import asyncio
import safygiphy
import requests
import random
import io
import time
import aiohttp
import os

client = discord.Client()

g = safygiphy.Giphy()
kicksid = "367805531169226775"

COR =0x690FC3
msg_id = None
msg_user = None
msg_author = None
qntdd = int
reaction_msg_stuff = {"role_msg_id": None, "role_msg_user_id": None, "r_role_msg_id": None, "r_role_msg_user_id": None}
BOTCOLOR = 0x547e34
version = "2.0.0"

is_prod = os.environ.get('IS_HEROKU', None)
if is_prod:
    token = os.environ.get('TOKEN')
else:
    import secreto
    token = secreto.token

def toint(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

@client.event
async def on_ready():
    print("=================================")
    print("Bot BITS iniciado com sucesso!")
    print (client.user.name)
    print (client.user.id)
    print(f"Bot Versão: {version}")
    print("=================================")
    await client.change_presence(game=discord.Game(name="!HELP", url='https://twitch.tv/TheDiretor', type=1))


@client.event
async def on_message(message):
# GERA UM CONVITE E ENVIA NO PRIVADO DE QUEM EXECUTOU O COMANDO
    if message.content.lower().startswith('!convite'):
        invite = await client.create_invite(message.channel, max_uses=1, xkcd=True)
        await client.send_message(message.author, "Olá, seu convite é {}".format(invite.url))
        await client.send_message(message.channel,
                                  "Olá {}, acabei de enviar um convite no seu privado.".format(message.author.mention))
# ALTERA O STATUS DE JOGO DO BOT
    if message.content.startswith('!jogando') and message.author.id == kicksid:
        game = message.content[9:]
        await client.change_presence(game=discord.Game(name=game))
        await client.send_message(message.channel, "Status de jogo alterado para: " + game + " ")

# MOEDA CARA OU COROA
    if message.content.lower().startswith('!moeda'):
        choice = random.randint(1, 2)
        if choice == 1:
            await client.add_reaction(message, '🌝')
        if choice == 2:
            await client.add_reaction(message, '👑')

# ROLE UM DADO
    if message.content.lower().startswith('!dado'):
        choice = random.randint(1, 6)
        embeddad = discord.Embed(title='Dado', description=' Joguei o dado, o resultado é :  {} 🎲'.format(choice),
                             colour=0x1abc9c)
        await client.send_message(message.channel, embed=embeddad)

# VEJA O MS DE CONEXÃO DO BOT
    if message.content.lower().startswith('!ping'):
      timep = time.time()
      emb = discord.Embed(title='Aguarde', color=0x565656)
      pingm0 = await client.send_message(message.channel, embed=emb)
      ping = time.time() - timep
      pingm1 = discord.Embed(title='Pong!', description=':ping_pong: Ping - %.01f segundos' % ping, color=0x15ff00)
      await client.edit_message(pingm0, embed=pingm1)

#BOT AVISA O QUE FOI DITO
    if message.content.lower().startswith("!say"):
        msg = message.content[5:2000]
        await client.send_message(message.channel, msg)
        await client.delete_message(message)

#PEGA O AVATAR DO USUÁRIO
    elif message.content.lower().startswith('!avatar'):
        try:
            membro = message.mentions[0]
            avatarembed = discord.Embed(
                title="",
                color=0xFF8000,
                description="**[Clique aqui](" + membro.avatar_url + ") para acessar o link de seu avatar!**"
            )
            avatarembed.set_author(name=membro.name)
            avatarembed.set_image(url=membro.avatar_url)
            await client.send_message(message.channel, embed=avatarembed)
        except:
            avatarembed2 = discord.Embed(
                title="",
                color=0xFF8000,
                description="**[Clique aqui](" + message.author.avatar_url + ") para acessar o link de seu avatar!**"
            )
            avatarembed2.set_author(name=message.author.name)
            avatarembed2.set_image(url=message.author.avatar_url)
            await client.send_message(message.channel, embed=avatarembed2)

# INICIA UMA VOTAÇÃO COM REAÇÃO DE LIKE E DESLIKE
    elif message.content.lower().startswith('!votar'):
        msg = message.content[7:2000]
        botmsg = await client.send_message(message.channel, msg)
        await client.add_reaction(botmsg, '👍')
        await client.add_reaction(botmsg, '👎')
        await client.delete_message(message)

# CANAL DE SUGESTOES, TODA MENSAGEM ENVIADA NESSE CANAL TEM ESSAS DUAS REAÇÕES AUTOMATICAMENTE
    if message.channel.id == ("425373271056449586"):
        await client.add_reaction(message, "✔")
        await client.add_reaction(message, "❌")

# CANAL DE POSTAGENS, TODA MENSAGEM ENVIADA NESSE CANAL TEM ESSAS DUAS REAÇÕES AUTOMATICAMENTE
    if message.channel.id == ("426747801935020033"):
        await client.add_reaction(message, "👍")
        await client.add_reaction(message, "👎")

# GERA UM GIF
    if message.content.startswith('!gif'):
        gif_tag = message.content[5:]
        rgif = g.random(tag=str(gif_tag))
        response = requests.get(
            str(rgif.get("data", {}).get('image_original_url')), stream=True
        )
        await client.send_file(message.channel, io.BytesIO(response.raw.read()), filename='video.gif')

# GERA UM GIF DIVERTIDO
    if message.content.startswith('!diversão'):
        gif_tag = "fun"
        rgif = g.random(tag=str(gif_tag))
        response = requests.get(
            str(rgif.get("data", {}).get('image_original_url')), stream=True
        )
        await client.send_file(message.channel, io.BytesIO(response.raw.read()), filename='video.gif')

# GERA UM GIF/VÍDEO ALEATÓRIO DE GATO
    if message.content.lower().startswith('!cat'):
        async with aiohttp.get('http://aws.random.cat/meow') as r:
            if r.status == 200:
                js = await r.json()
                canal = message.channel
                await client.delete_message(message)
                await client.send_message(canal, js['file'])

# GERA UM GIF/VÍDEO ALEATÓRIO DE CACHORRO
    if message.content.lower().startswith('!dog'):
        async with aiohttp.get('https://random.dog/woof.json') as r:
            if r.status == 200:
                js = await r.json()
                canal = message.channel
                await client.delete_message(message)
                await client.send_message(canal, js['url'])

#BANE UM MEMBRO
    elif message.content.lower().startswith('!ban'):
        membro = message.mentions[0]
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, "❌ {} Você nao possui permissão para executar este comando!".format(message.author.mention))

        await client.send_message(message.channel, "✔ O staff {} Baniu o membro {}!".format(message.author.mention, message.mentions[0].mention))
        await client.ban(membro)

#KICKA UM MEMBRO
    elif message.content.lower().startswith('!kick'):
        member = message.mentions[0]
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, "❌ {} Você nao possui permissão para executar este comando!".format(message.author.mention))

        await client.send_message(message.channel, "✔ O staff {} expulsou o membro {}!".format(message.author.mention, message.mentions[0].mention))
        await client.kick(member)

#MUTA UM MEMBRO
    elif message.content.lower().startswith('!mute'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui permissão para executar este comando!')
        mention = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='Mutado')
        await client.add_roles(mention, cargo)
        await client.send_message(message.channel, '✔ O membro {} foi mutado com sucesso!'.format(mention))

#DESMUTA UM MEMBRO
    elif message.content.lower().startswith('!unmute'):
        if not message.author.server_permissions.administrator:
            return await client.send_message(message.channel, '❌ Você não possui permissão para executar este comando!')
        mention = message.mentions[0]
        cargo = discord.utils.get(message.author.server.roles, name='Mutado')
        await client.remove_roles(mention, cargo)
        await client.send_message(message.channel, '✔ O membro {} foi desmutado com sucesso!'.format(mention))

# INFORMAÇÕES DO BOT NO PRIVADO
    if message.content.lower().startswith('!help'):
        embed = discord.Embed(
            title="Meus comandos:",
            color=0xe67e22,
            description="***!moeda*** » Aposte com seu amigo no cara ou coroa.\n"
                        "***!user*** `<usuário>` » Veja as informações do usuário.\n"
                        "***!convite*** » Pegue nosso convite e espalhe para novas pessoas. \n"
                        "***!ping*** » Veja o meu ping. \n"
                        "***!cargo*** » Escolha um cargo entre aluno ou membro. \n"
                        "***!gif*** `<tag do gif (de preferencia em inglês)>` » Gere um GIF aleátorio. \n"
                        "***!dado*** » Role um dado com um número de 1 a 6. \n"
                        "***!dog*** » Gere um gif/vídeo de um cachorro. \n"
                        "***!cat*** » Gere um gif/vídeo de um gato. \n"
                        "***!avatar*** `<usuário>` » Veja a foto de perfil de um usuário."
        )
        embed.set_author(
            name="BITS",
            icon_url="https://cdn.discordapp.com/attachments/413336082579718155/413343990058844160/Perfil-BIts.png",
            url="https://twitter.com/brunoqq_"
        )
        embed.set_footer(
            text="Copyright © 2018 Bruno",
            icon_url="https://cdn.discordapp.com/emojis/412576344120229888.png?v=1"
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/413336082579718155/413343990058844160/Perfil-BIts.png"
        )

        await client.send_message(message.channel, "Olá {}, te enviei minhas informações no seu privado!".format(message.author.mention))
        await client.send_message(message.author, embed=embed)

# INFO DO SERVIDOR
    if message.content.lower().startswith('!serverinfo'):
        server = message.server
        embedserver = discord.Embed(
            title='Informaçoes do Servidor',
            color=0x551A8B,
            descripition='Essas são as informaçoes\n')
        embedserver = discord.Embed(name="{} Server ".format(message.server.name), color=0x551A8B)
        embedserver.add_field(name="Nome:", value=message.server.name, inline=True)
        embedserver.add_field(name="Dono:", value=message.server.owner.mention)
        embedserver.add_field(name="ID:", value=message.server.id, inline=True)
        embedserver.add_field(name="Cargos:", value=len(message.server.roles), inline=True)
        embedserver.add_field(name="Membros:", value=len(message.server.members), inline=True)
        embedserver.add_field(name="Criado em:", value=message.server.created_at.strftime("%d %b %Y %H:%M"))
        embedserver.add_field(name="Emojis:", value=f"{len(message.server.emojis)}/100")
        embedserver.add_field(name="Região:", value=str(message.server.region).title())
        embedserver.set_thumbnail(url=message.server.icon_url)
        embedserver.set_footer(text="By: brunoqq")
        await client.send_message(message.channel, embed=embedserver)

# PEGA INFORMAÇÕES DO USUÁRIO
    if message.content.startswith('!user'):
        try:
            user = message.mentions[0]
            userjoinedat = str(user.joined_at).split('.', 1)[0]
            usercreatedat = str(user.created_at).split('.', 1)[0]

            userembed = discord.Embed(
                title="Nome:",
                description=user.name,
                color=0xe67e22
            )
            userembed.set_author(
                name="Informações do usuário"
            )
            userembed.add_field(
                name="Entrou no BITS servidor em:",
                value=userjoinedat
            )
            userembed.add_field(
                name="Criou seu Discord em:",
                value=usercreatedat
            )
            userembed.add_field(
                name="TAG:",
                value=user.discriminator
            )
            userembed.add_field(
                name="ID:",
                value=user.id
            )

            await client.send_message(message.channel, embed=userembed)
        except IndexError:
            await client.send_message(message.channel, "Usuário não encontrado!")
        except:
            await client.send_message(message.channel, "Erro, desculpe. ")
        finally:
            pass

# APAGA DE 1 A 100 MENSAGENS
    if message.content.lower().startswith('!apagar'):
        qntdd = message.content.strip('!apagar ')
        qntdd = toint(qntdd)

        cargo = discord.utils.find(lambda r: r.name == "💻 Developer", message.server.roles)

        if message.author.top_role.position >= cargo.position:
            if qntdd <= 100:
                msg_author = message.author.mention
                await client.delete_message(message)
                # await asyncio.sleep(1)
                deleted = await client.purge_from(message.channel, limit=qntdd)
                botmsgdelete = await client.send_message(message.channel,
                                                         '{} mensagens foram excluidas com sucesso, {}.'.format(
                                                             len(deleted), msg_author))
                await asyncio.sleep(5)
                await client.delete_message(botmsgdelete)

            else:
                botmsgdelete = await client.send_message(message.channel,
                                                         'Utilize o comando digitando !apagar <numero de 1 a 100>.')
                await asyncio.sleep(5)
                await client.delete_message(message)
                await client.delete_message(botmsgdelete)

        else:
            await client.send_message(message.channel, 'Você não tem permissão para utilizar este comando.')

# ADICIONA O CARGO POR REAÇÃO
    if message.content.lower().startswith("!cargo"):
        embed1 = discord.Embed(
            title="Escolha seu cargo:",
            color=COR,
            description="Aluno = 📒\n"
                        "Membro = 💬", )

    botmsg = await client.send_message(message.channel, embed=embed1)

    await client.add_reaction(botmsg, "📒")
    await client.add_reaction(botmsg, "💬")

    global msg_id
    msg_id = botmsg.id

    global msg_user
    msg_user = message.author


@client.event
async def on_reaction_add(reaction, user):
    msg = reaction.message

    if reaction.emoji == "📒" and msg.id == msg_id:  # and user == msg_user:
        role = discord.utils.find(lambda r: r.name == "📒 Aluno", msg.server.roles)
        await client.add_roles(user, role)
        print("add")

    if reaction.emoji == "💬" and msg.id == msg_id:  # and user == msg_user:
        role = discord.utils.find(lambda r: r.name == "💬 Membro", msg.server.roles)
        await client.add_roles(user, role)
        print("add")

@client.event
async def on_reaction_remove(reaction, user):
    msg = reaction.message

    if reaction.emoji == "📒" and msg.id == msg_id:  # and user == msg_user:
        role = discord.utils.find(lambda r: r.name == "📒 Aluno", msg.server.roles)
        await client.remove_roles(user, role)
        print("remove")

    if reaction.emoji == "💬" and msg.id == msg_id:  # and user == msg_user:
        role = discord.utils.find(lambda r: r.name == "💬 Membro", msg.server.roles)
        await client.remove_roles(user, role)
        print("remove")

#AO ENTRAR NO SERVIDOR ELE ENVIA MENSAGEM NO PRIVADO, SETA ROLE MEMBRO E ENVIA MENSAGEM NO CANAL DO DISCORD
@client.event
async def on_member_join(member):

      await client.send_message(member, "Seja bem vindo ao nosso Discord! Qualquer dúvida, sugestões ou bugs contate um de nossos fundadores Kicks🌊#9493, Sevinhu#6136 ou Fury#3740.")
      grupo = discord.utils.find(lambda g: g.name == "💬 Membro", member.server.roles)
      await client.add_roles(member, grupo)

      channel = client.get_channel('413348837718229043')
      serverchannel = member.server.default_channel
      msg = "Seja bem vindo ao servidor {0}, divirta-se!".format(member.mention, member.server.name)
      await client.send_message(channel, msg)

# MENSAGEM QUANDO ALGUÉM SAI DO SERVIDOR
@client.event
async def on_member_remove(member):

    channel = client.get_channel('425369911267819521')
    serverchannel = member.server.default_channel
    msg = "{0} acabou de sair do servidor, alguém o resgate-o!".format(member.name)
    await client.send_message(channel, msg)

client.run(token)
