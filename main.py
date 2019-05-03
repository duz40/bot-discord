#!/usr/bin/env python
# -*- coding: utf-8 -*-

# USE PIP3 INSTALL DISCORD PARA IMPORTAR, OU BAIXE E JOGUE NO PROJETO (PYTHON 3.6)

import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import string
import random
import urllib.request
import json
import requests
import http.client
from igdb_api_python.igdb import igdb

from tokens import CLIENT
from commands import BOT_COMMANDS
from mapsOW import MAPS_DICT

igdb = igdb("419d086db966b98459e547592d0155bf")

Client = discord.Client()
client = commands.Bot(command_prefix="&")


@client.event
async def on_ready():
    print("Bot online!")


@client.event
async def on_message(message):
    # Prevenir loop de respostas
    if message.author == client.user:
        return

    # comandos básicos:
    if message.content.lower().startswith("oi bot"):
        msg = 'Olá {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.lower() == "&commands":
        msg = "**O que posso fazer até agora {0.author.mention} :**\n\n".format(message)
        await client.send_message(message.author, msg + BOT_COMMANDS)

    if 'bot' in message.content.lower() and 'burro' in message.content.lower():
        await client.send_message(message.channel, "Para que esta agressão? toma um biscoito: :cookie:")
        await client.add_reaction(message, '😢')

    if message.content.lower() == "&praise the sun":
        gif = discord.Embed(title="", description="", color=0x32363c)
        url_praise = "https://i.imgur.com/xZ2sEbd.gif?noredirect"
        gif.set_image(url=url_praise)
        await client.send_message(message.channel, url_praise, embed=gif)

    # Imagens/gifs
    if message.content.lower() == "&socorro":
        imagem = discord.Embed(title="", description="", color=0x32363c)
        json_cat = json.loads(urllib.request.urlopen("http://aws.random.cat/meow").read())
        cat_photo = json.dumps(json_cat["file"]).strip("\"")
        imagem.set_image(url=cat_photo)
        await client.send_message(message.channel, cat_photo, embed=imagem)
    if message.content.lower() == "&meacuda":
        imagem = discord.Embed(title="", description="", color=0x32363c)
        json_cat_gif = json.loads(
            urllib.request.urlopen("http://thecatapi.com/api/images/get?format=json&type=gif").read())
        # print(json_cat_gif)
        cat_gif = json.dumps(json_cat_gif[0]["url"]).strip("\"")
        imagem.set_image(url=cat_gif)
        await client.send_message(message.channel, cat_gif, embed=imagem)

    # Piadas
    message_array = message.content.lower().split()
    trigger_words = ['bot', 'conta', 'piada']
    if all([word in message.content.lower() for word in trigger_words]):
        url_pave = "https://www.reddit.com/r/tiodopave/random.json"
        url_charada = "https://us-central1-kivson.cloudfunctions.net/charada-aleatoria"
        url = random.choice([url_pave, url_charada])
        if url == url_charada:
            try:
                print("url_charada")
                json_charada = requests.get(url, headers={'Accept': 'application/json'}).json()
                text_title = json_charada['pergunta']
                text_content = json_charada['resposta']
                await client.send_message(message.channel, str(text_title) + "\n\n" + str(text_content) + "\n")
            except:
                await client.send_message(message.channel, "to pensando, pergunta de novo!")
        if url == url_pave:
            try:
                print("url_tio_do_pave")
                # json_piada = json.loads(urllib.request.urlopen(url).read())
                random_agent = random.randint(0, 10000)
                json_piada = requests.get(url, headers={
                    'User-agent': 'bot discord restart jogatina ' + str(random_agent)}).json()
                # print(json_piada)
                text_title = json_piada[0]["data"]["children"][0]["data"]["title"]
                text_content = json_piada[0]["data"]["children"][0]["data"]["selftext"]
                await client.send_message(message.channel, str(text_title) + "\n\n" + str(text_content) + "\n")
            except:
                await client.send_message(message.channel, "to pensando, pergunta de novo!")

    # GAMES API
    if message.content.lower().startswith("&game"):
        args = message.content.split(" ")
        if len(args) >= 3 and args[1] == "info":
            game_name = igdb.games({
                'search': args[2:],
                'fields': 'name'
            })
            game_req = igdb.games(game_name.body[0]["id"])
            company_name = ""
            if 'developers' in game_req.body[0]:
                company_id = igdb.companies(game_req.body[0]["developers"][0])
                company_name = company_id.body[0]["name"]
            game_info = game_req.body[0]
            site = ""
            rating = "--"
            if 'total_rating' in game_info:
                rating = str(int(game_info["total_rating"]))
            date = "ND"
            if 'release_dates' in game_info:
                date = game_info["release_dates"][0]["y"]
            if "websites" in game_info:
                for x in game_info["websites"]:
                    if "category" in x and x["category"] == 13:
                        site = x["url"]
                    elif "category" in x and x["category"] == 1:
                        site = x["url"]
                    elif "category" in x and x["category"] == 3:
                        site = x["url"]
                    elif "category" in x and x["category"] == 4:
                        site = x["url"]
                    elif "category" in x and x["category"] == random.choice([2, 5, 6, 7, 8, 9, 10, 11, 12, 14]):
                        site = x["url"]
            cover_thumb = "https://www.tecomat.cz/uploads/Products/no-image.png"
            if 'cover' in game_info:
                cover_thumb = "https:" + game_info["cover"]["url"]
            embed = discord.Embed(title=game_info["name"],
                                  url=site,
                                  description=game_info["summary"],
                                  color=0xff0000)
            embed.set_thumbnail(url=cover_thumb)
            embed.add_field(name="Ano", value=str(date), inline=True)
            embed.add_field(name="score", value=rating, inline=True)
            embed.set_footer(text=company_name)
            await client.send_message(message.channel, "aqui está!", embed=embed)

        elif len(args) >= 2:
            result = igdb.games({
                'search': args[1:],
                'fields': 'name'
            })
            games_string = ""
            for game in result.body:
                games_string = games_string + str(game["name"]) + "\n"
            await client.send_message(message.channel, "Achei esses jogos na base de dados:\n\n" + games_string)

    # OVERWATCH API (UNOFFICIAL)
    if message.content.lower().startswith("&owstats"):
        args = message.content.split(" ")
        if len(args) == 3:
            stats_url = "http://ow-api.herokuapp.com/stats/pc/us/" + args[1]
            try:
                ow_stats = requests.get(stats_url).json()

                hero_name = args[2].lower()
                hero_name.replace("-", " ")

                heroes = ow_stats["stats"]["top_heroes"]
                hero_pic = "https://www.tecomat.cz/uploads/Products/no-image.png"
                played_time = ""
                for x in heroes["quickplay"]["played"]:
                    if 'hero' in x and x['hero'].lower() == hero_name:
                        hero_pic = x['img']
                        played_time = x['played']
                        break
                games_won = ""
                for x in heroes["quickplay"]["games_won"]:
                    if 'hero' in x and x['hero'].lower() == hero_name:
                        games_won = x['games_won']
                        break
                weapon_accuracy = ""
                for x in heroes["quickplay"]["weapon_accuracy"]:
                    if 'hero' in x and x['hero'].lower() == hero_name:
                        weapon_accuracy = x['weapon_accuracy']
                        break
                eliminations_per_life = ""
                for x in heroes["quickplay"]["eliminations_per_life"]:
                    if 'hero' in x and x['hero'].lower() == hero_name:
                        eliminations_per_life = x['eliminations_per_life']
                        break
                embed_stats = discord.Embed(title=hero_name.capitalize(),
                                            description="",
                                            color=0xff0000)
                embed_stats.set_author(name=ow_stats["username"].capitalize())
                embed_stats.set_thumbnail(url=hero_pic)
                embed_stats.add_field(name="Horas jogadas", value=played_time, inline=True)
                embed_stats.add_field(name="Jogos ganhos", value=games_won, inline=True)
                embed_stats.add_field(name="Precisão da arma", value=weapon_accuracy, inline=True)
                embed_stats.add_field(name="K/D", value=eliminations_per_life, inline=True)
                msg = "Aqui está!".format(message)
                await client.send_message(message.channel, msg, embed=embed_stats)
            except:
                await client.send_message(message.channel, "Algo aconteceu e não achei o herói.")
        elif len(args) == 4:
            if args[3] == "compfull":
                tech_url = "https://owapi.net/api/v3/u/" + args[1] + "/heroes"
                try:
                    ow_hero_request = requests.get(tech_url, headers={"User-Agent": "owapi discord bot stats"}).json()
                    hero_stats = ow_hero_request["us"]["heroes"]["stats"]["competitive"]
                    hero_name = args[2]
                    stats_info = ""
                    stats_info = "**" + args[1].split("-")[0].capitalize() + "**\n\n"
                    stats_info += "[" + args[2].capitalize() + ":](https://www.overbuff.com/players/pc/" + args[
                        1] + "/heroes/" + args[2] + "?mode=competitive)\n\n"
                    if hero_name in hero_stats:
                        role_stats = hero_stats[hero_name]["general_stats"]
                    for x in role_stats.keys():
                        stats_info += str(x).replace("_", " ") + " - **" + str(round(role_stats[x], 3)) + "**\n"

                    embed_hero_tech = discord.Embed(title=" ", description=stats_info, color=0xf99e1a)
                    await client.send_message(message.channel, embed=embed_hero_tech)

                except:
                    await client.send_message(message.channel, "Algo aconteceu e não achei o herói.")
            else:
                stats_url = "http://ow-api.herokuapp.com/stats/pc/us/" + args[1]
                try:
                    ow_stats = requests.get(stats_url).json()

                    hero_name = args[2].lower()
                    hero_name.replace("-", " ")

                    heroes = ow_stats["stats"]["top_heroes"]
                    hero_pic = "https://www.tecomat.cz/uploads/Products/no-image.png"
                    played_time = ""
                    for x in heroes["competitive"]["played"]:
                        if 'hero' in x and x['hero'].lower() == hero_name:
                            hero_pic = x['img']
                            played_time = x['played']
                            break
                    games_won = ""
                    for x in heroes["competitive"]["games_won"]:
                        if 'hero' in x and x['hero'].lower() == hero_name:
                            games_won = x['games_won']
                            break
                    weapon_accuracy = ""
                    for x in heroes["competitive"]["weapon_accuracy"]:
                        if 'hero' in x and x['hero'].lower() == hero_name:
                            weapon_accuracy = x['weapon_accuracy']
                            break
                    eliminations_per_life = ""
                    for x in heroes["competitive"]["eliminations_per_life"]:
                        if 'hero' in x and x['hero'].lower() == hero_name:
                            eliminations_per_life = x['eliminations_per_life']
                            break
                    embed_stats = discord.Embed(title=hero_name.capitalize(),
                                                description="COMPETITIVE",
                                                color=0xff0000)
                    embed_stats.set_author(name=ow_stats["username"].capitalize())
                    embed_stats.set_thumbnail(url=hero_pic)
                    embed_stats.add_field(name="Horas jogadas", value=played_time, inline=True)
                    embed_stats.add_field(name="Jogos ganhos", value=games_won, inline=True)
                    embed_stats.add_field(name="Precisão da arma", value=weapon_accuracy, inline=True)
                    embed_stats.add_field(name="K/D", value=eliminations_per_life, inline=True)
                    msg = "Aqui está!".format(message)
                    await client.send_message(message.channel, msg, embed=embed_stats)
                except:
                    await client.send_message(message.channel, "Algo aconteceu e não achei o herói.")
        else:
            owurl = "http://ow-api.herokuapp.com/profile/pc/us/" + args[1]
            try:
                ow_profile = requests.get(owurl).json()
                usr_rank = "--"
                rank_img = ""
                comp_won = "--"
                comp_lost = "--"
                comp_draw = "--"
                comp_time = "--"
                if "competitive" in ow_profile["playtime"]:
                    comp_time = str(ow_profile["playtime"]["competitive"])
                if "competitive" in ow_profile:
                    if "rank" in ow_profile["competitive"] and ow_profile["competitive"]["rank"] is not None:
                        usr_rank = ow_profile["competitive"]["rank"]
                        if "won" in ow_profile["games"]["competitive"]:
                            comp_won = str(ow_profile["games"]["competitive"]["won"])
                        if "lost" in ow_profile["games"]["competitive"]:
                            comp_lost = str(ow_profile["games"]["competitive"]["lost"])
                        if "draw" in ow_profile["games"]["competitive"]:
                            comp_draw = str(ow_profile["games"]["competitive"]["draw"])
                        if "rank_img" in ow_profile["competitive"]:
                            rank_img = ow_profile["competitive"]["rank_img"]
                embed_msg = discord.Embed(title="Rank",
                                          description=str(usr_rank),
                                          color=0xff0000)
                embed_msg.set_author(name=ow_profile["username"], icon_url=rank_img)
                embed_msg.set_thumbnail(url=ow_profile["portrait"])
                embed_msg.add_field(name="Level", value=str(ow_profile["level"]), inline=True)
                embed_msg.add_field(name="Tempo Quick", value=str(ow_profile["playtime"]["quickplay"]), inline=True)
                embed_msg.add_field(name="Jogos Quick", value="ganhou: " + str(ow_profile["games"]["quickplay"]["won"]),
                                    inline=True)
                embed_msg.add_field(name="Tempo Comp", value=comp_time, inline=True)
                embed_msg.add_field(name="Jogos Comp", value="ganhou: " + comp_won, inline=True)
                embed_msg.add_field(name="Jogos Comp", value="perdeu: " + comp_lost, inline=True)
                embed_msg.add_field(name="Jogos Comp", value="draw: " + comp_draw, inline=True)
                msg = "Achei o perfil!".format(message)
                # await client.send_message(message.channel, msg, embed=embed_msg)

                alt_msg = "**Rank:**\n\n"
                alt_msg += str(usr_rank) + "\n\n"
                alt_msg += "**Level:**\n\n"
                alt_msg += str(ow_profile["level"]) + "\n\n"
                alt_msg += "**Quickplay:**\n\n"
                alt_msg += "• Tempo: " + str(ow_profile["playtime"]["quickplay"]) + "\n"
                alt_msg += "• Ganhou: " + str(ow_profile["games"]["quickplay"]["won"]) + "\n\n"
                alt_msg += "**Competitive:**\n\n"
                alt_msg += "• Tempo: " + comp_time + "\n"
                alt_msg += "• Ganhou: " + comp_won + "\n"
                alt_msg += "• Perdeu: " + comp_lost + "\n"
                alt_msg += "• Empate: " + comp_draw

                embed_alt = discord.Embed(title=" ", description=alt_msg)
                embed_alt.set_author(name=ow_profile["username"], icon_url=rank_img)
                embed_alt.set_thumbnail(url=ow_profile["portrait"])
                await client.send_message(message.channel, embed=embed_alt)

            except:
                await client.send_message(message.channel, "Não achei o perfil, ou ele está privado")

    if message.content.lower().startswith("&owmaps"):
        args = message.content.split(" ")
        if len(args) > 1:
            try:
                maps = " ".join(args[1:]).lower()
                if maps in MAPS_DICT:
                    with open(MAPS_DICT[maps], 'rb') as picture:
                        await client.send_file(message.channel, picture)
            except:
                await client.send_message(message.channel, "Não achei o mapa...")

    # STEAM API
    if message.content.lower().startswith("&steam"):
        args = message.content.split(" ")
        game_name = ' '.join(args[1:])
        appreq = requests.get("http://api.steampowered.com/ISteamApps/GetAppList/v0001/").json()
        applist = appreq['applist']['apps']['app']
        try:
            game_id = 0
            for x in applist:
                if x["name"].lower() == game_name.lower():
                    print("Achou!")
                    print(x["name"])
                    print(x["appid"])
                    game_id = str(x["appid"])
                    break
            steamapp_url = "https://store.steampowered.com/api/appdetails?cc=br&appids=" + game_id
            game_req = requests.get(steamapp_url).json()
            if game_req[game_id]["success"] is True:
                game_info = game_req[game_id]["data"]
            else:
                return

            game_url = "http://store.steampowered.com/app/" + str(game_info["steam_appid"])
            thumb_url = game_info["header_image"]
            metacritic = "--"
            if "metacritic" in game_info:
                metacritic = game_info["metacritic"]["score"]
            embed = discord.Embed(title=game_info["name"],
                                  url=game_url,
                                  description=game_info["short_description"],
                                  color=0xff0000)
            embed.set_thumbnail(url=thumb_url)
            embed.add_field(name="Ano", value=str(game_info["release_date"]["date"]), inline=True)
            embed.add_field(name="metacritic", value=metacritic, inline=True)
            if game_info["price_overview"]["initial"] == game_info["price_overview"]["final"]:
                embed.add_field(name="Preço", value=str(game_info["price_overview"]["final_formatted"]), inline=True)
            else:
                percent = str(game_info["price_overview"]["discount_percent"]) + '%'
                embed.add_field(name="PROMOÇÃO " + percent, value=str(game_info["price_overview"]["final_formatted"]),
                                inline=False)
            embed.set_footer(text=game_info["publishers"][0])
            for x in game_info["categories"]:
                if x["id"] == 1:
                    embed.add_field(name="Multi-player?", value="sim", inline=True)
                if x["id"] == 9:
                    embed.add_field(name="Co-op?", value="sim", inline=True)
                if x["id"] == 38:
                    embed.add_field(name="Online Co-op?", value="sim", inline=True)
            await client.send_message(message.channel, "aqui está!", embed=embed)
        except:
            await client.send_message(message.channel, "Não achei o jogo...")

    if message.content.lower() == "&promosteam":
        try:
            featured_url = "https://store.steampowered.com/api/featuredcategories/?cc=br"
            result = requests.get(featured_url).json()
            promos = result["specials"]["items"]
            promo_games = ""
            for game in promos:
                game_url = "http://store.steampowered.com/app/" + str(game["id"])
                percent = str(game["discount_percent"]) + "%"
                price = str(game["final_price"])
                size = len(price) - 2
                preco_br = " - R$ " + price[:size] + "," + price[2:]
                promo_games += "[" + game["name"] + "](" + game_url + ")" + preco_br + " **(" + percent + ")**\n"

            embed = discord.Embed(title="Principais jogos em promoção:", description=promo_games)

            await client.send_message(message.channel, embed=embed)

        except:
            await client.send_message(message.channel, "Algo deu errado...")

    if message.content.lower().startswith("&horapminutos"):
        args = message.content.split(" ")
        args[1] = args[1].replace(",", ".")
        num = float(args[1])
        minutes = 60 * num
        minutes_to_show = int(minutes)
        sec = 60 * (minutes % 1)
        seconds_to_show = str(int(sec))
        await client.send_message(message.channel, str(minutes_to_show) + ":" + str(seconds_to_show))


@client.event
async def on_voice_state_update(before, after):
    if before.voice.voice_channel is None and after.voice.voice_channel is not None:
        for channel in after.server.channels:
            if channel.name == 'overwatch' and after.voice.voice_channel.id == "318045974062825495" and len(
                    after.voice.voice_channel.voice_members) == 1:
                # print(after.voice.voice_channel.id)
                # print(len(after.voice.voice_channel.voice_members))
                msg = "{0.name} entrou no chat de voz!".format(after)
                await client.send_message(channel, msg)
            elif channel.name == 'miop' and after.voice.voice_channel.name == 'MIOP' and len(
                    after.voice.voice_channel.voice_members) == 1:
                msg = "{0.name} entrou no chat de voz...".format(after)
                # print(msg)
                await client.send_message(channel, msg)


# if before.voice.voice_channel is not None and after.voice.voice_channel is None:
# 	for channel in before.server.channels:
# 		if channel.name == 'overwatch' and before.voice.voice_channel.id == "318045974062825495":
# 			msg = "<@&330452643145187340> , {0.mention} saiu do chat de voz...".format(before)
# 			# print(msg)
# 			await client.send_message(channel, msg)
# 		elif channel.name == 'miop' and before.voice.voice_channel.name == 'MIOP':
# 			msg = "@here , {0.mention} saiu do chat de voz...".format(before)
# 			# print(msg)
# 			await client.send_message(channel, msg)


# Descomente o comando abaixo e adicione a token do bot teste!
# client.run("NTA2NTI1NjUxMjQ4MDg3MDUw.DrjafQ.fEZiYDARFRj35oLLMHcwohR-njU")
# token bot jogatina
client.run(CLIENT)

# "C:\Users\duz40\AppData\Local\Programs\Python\Python36\python.exe" sampleBot.py

# Greetings
# if message.content.startswith('hello'):
# msg = 'Hello {0.author.mention}'.format(message)
# await client.send_message(message.channel, msg)