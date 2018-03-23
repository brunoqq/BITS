import discord
import asyncio
import safygiphy
import requests
import random
import io

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
version = "Beta 1.0.0"

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
    if message.content.lower().startswith('!convite'):
        invite = await client.create_invite(message.channel, max_uses=1, xkcd=True)
        await client.send_message(message.author, "Olá, seu convite é {}".format(invite.url))
        await client.send_message(message.channel,
                                  "Olá {}, acabei de enviar um convite no seu privado.".format(message.author.mention))

    if message.content.startswith('!jogando') and message.author.id == kicksid:
        game = message.content[9:]
        await client.change_presence(game=discord.Game(name=game))
        await client.send_message(message.channel, "Status de jogo alterado para: " + game + " ")

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
    if message.content.lower().startswith('!help'):
        embed = discord.Embed(
            title="Meus comandos:",
            color=0xe67e22,
            description="***!moeda*** » Aposte com seu amigo no cara ou coroa.\n"
                        "***!user*** `<usuário>` » Veja as informações do usuário.\n"
                        "***!convite*** » Pegue nosso convite e espalhe para novas pessoas. \n"
                        "***!gif*** » Gere um GIF aleátorio. \n"
                        "Estou na versão Beta 1.0.0, em breve uma ótima atualização."
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

    if message.content.startswith('!gif'):
        gif_tag = message.content[5:]
        rgif = g.random(tag=str(gif_tag))
        response = requests.get(
            str(rgif.get("data", {}).get('image_original_url')), stream=True
        )
        await client.send_file(message.channel, io.BytesIO(response.raw.read()), filename='video.gif')

    if message.content.startswith('!diversão'):
        gif_tag = "fun"
        rgif = g.random(tag=str(gif_tag))
        response = requests.get(
            str(rgif.get("data", {}).get('image_original_url')), stream=True
        )
        await client.send_file(message.channel, io.BytesIO(response.raw.read()), filename='video.gif')

    if message.content.lower().startswith('!moeda'):
        choice = random.randint(1, 2)
        if choice == 1:
            await client.add_reaction(message, '🌝')
        if choice == 2:
            await client.add_reaction(message, '👑')

    if message.channel.id == ("425373271056449586"):
        await client.add_reaction(message, "✔")
        await client.add_reaction(message, "❌")
        
    if message.channel.id == ("426747801935020033"):
        await client.add_reaction(message, "👍")
        await client.add_reaction(message, "👎")

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

@client.event
async def on_member_join(member):

      await client.send_message(member, "Seja bem vindo ao nosso Discord! Qualquer dúvida, sugestões ou bugs contate um de nossos fundadores Kicks🌊#9493, Sevinhu#6136 ou Fury#3740.")
      grupo = discord.utils.find(lambda g: g.name == "💬 Membro", member.server.roles)
      await client.add_roles(member, grupo)

      channel = client.get_channel('413348837718229043')
      serverchannel = member.server.default_channel
      msg = "Seja bem vindo ao servidor {0}, divirta-se!".format(member.mention, member.server.name)
      await client.send_message(channel, msg)

@client.event
async def on_member_remove(member):

    channel = client.get_channel('425369911267819521')
    serverchannel = member.server.default_channel
    msg = "{0} acabou de sair do servidor, alguém resgate-o!".format(member.name)
    await client.send_message(channel, msg)

client.run('NDI1Mzc5MTk2NzM5NTE4NDc1.DZM5OA.gu11m6STl6Iyrg2KzyLLOq_cf-s')
