import discord, json, os, datetime
from discord import option

with open(os.getcwd() + '/Config.json') as f:
    config = json.load(f)

intents = discord.Intents().all()
intents.message_content = True
client = discord.Bot(intents=intents)

points = client.create_group("points")
vouch = client.create_group("vouch")

@client.event
async def on_ready():
    print("Bot is ready!")

users = {}

with open(os.getcwd() + "/Points.json") as f:
    users = json.load(f)

vouches = {}

with open(os.getcwd() + '/Vouches.json') as f:
    vouches = json.load(f)

@points.command(description = "Get Points")
async def total(ctx: discord.ApplicationContext, member: discord.Member):
    with open(os.getcwd() + '/Points.json') as f:
        users = json.load(f)
    
    for user in users:
        if user == str(member.id):

            embed = discord.Embed(title = "Success Rewards", color = config['embed_color'])
            embed.add_field(name = "Total Points", value = f"{users[user]} points!")
            embed.set_footer(text = config["embed_text"], icon_url=config["embed_icon"])

            await ctx.respond(embed = embed)
            return
    
    embed = discord.Embed(title = "Success Rewards", color = config['embed_color'])
    embed.add_field(name = "Total Points", value = f"0 points!")
    embed.set_footer(text = config["embed_text"], icon_url=config["embed_icon"])

    await ctx.respond(embed = embed)
    return

@points.command(description = "Add Points")
async def add(ctx: discord.ApplicationContext, member: discord.Member, points: int):
    with open(os.getcwd() + '/Points.json') as f:
        users = json.load(f)
    
    for user in users:
        if user == str(member.id):
            users[user] += points

            with open(os.getcwd() + "/Points.json", "w") as f:
                json.dump(users, f, indent=4)

            embed = discord.Embed(title = "Success Rewards", color = config['embed_color'])
            embed.add_field(name = "Total Points", value = f"{users[user]} points!")
            embed.set_footer(text = config["embed_text"], icon_url=config["embed_icon"])

            await ctx.respond(embed = embed)
            return
    
    embed = discord.Embed(title = "Success Rewards", color = config['embed_color'])
    embed.add_field(name = "Total Points", value = f"0 points!")
    embed.set_footer(text = config["embed_text"], icon_url=config["embed_icon"])

    await ctx.respond(embed = embed)
    return

@points.command(description = "Remove Points")
async def remove(ctx: discord.ApplicationContext, member: discord.Member, points: int):
    with open(os.getcwd() + '/Points.json') as f:
        users = json.load(f)
    
    for user in users:
        if user == str(member.id):
            users[user] -= points

            with open(os.getcwd() + "/Points.json", "w") as f:
                json.dump(users, f, indent=4)

            embed = discord.Embed(title = "Success Rewards", color = config['embed_color'])
            embed.add_field(name = "Total Points", value = f"{users[user]} points!")
            embed.set_footer(text = config["embed_text"], icon_url=config["embed_icon"])

            await ctx.respond(embed = embed)
            return
    
    embed = discord.Embed(title = "Success Rewards", color = config['embed_color'])
    embed.add_field(name = "Total Points", value = f"0 points!")
    embed.set_footer(text = config["embed_text"], icon_url=config["embed_icon"])

    await ctx.respond(embed = embed)
    return

@points.command(description = "Points Leaderboard")
async def leaderboard(ctx: discord.ApplicationContext):
    with open(os.getcwd() + '/Points.json') as f:
        users = json.load(f)

    sorted_users = sorted(users.items(), key=lambda x: x[1], reverse=True)

    description = ""

    embed = discord.Embed(title = "Success Rewards", color = config['embed_color'])

    for i, (user_id, score) in enumerate(sorted_users[:10]):
        user = ctx.guild.get_member(int(user_id))
        if user is None:
            continue

        description += f"#{i+1}: {user.name} - {score} points\n"
    
    embed.add_field(name = "Leaderboard", value = description)
    embed.set_footer(text = config["embed_text"], icon_url=config["embed_icon"])
    await ctx.respond(embed=embed)
    
@client.event
async def on_message(message):
    if message.channel.id == config['channel_id'] and message.author.id != client.user.id:
        if 'https://twitter.com' in message.content:
            if str(message.author.id) in users:
                users[str(message.author.id)] += config['twitter_points']
            else:
                users[str(message.author.id)] = config['twitter_points']
            
            with open(os.getcwd() + "/Points.json", "w") as f:
                json.dump(users, f, indent=4)

            await message.add_reaction('✅')

            embed = discord.Embed(title = "Success Rewards", color = config['embed_color'])
            embed.add_field(name = "Twitter", value = f"You have earned 5 points!")
            embed.add_field(name = "Total Points", value = users[str(message.author.id)], inline=False)
            embed.set_footer(text = config["embed_text"], icon_url=config["embed_icon"])

            await message.reply(embed = embed)

            return
    
        elif message.attachments:
            if str(message.author.id) in users:
                users[str(message.author.id)] += config['image_points']
            else:
                users[str(message.author.id)] = config['image_points']

            with open(os.getcwd() + "/Points.json", "w") as f:
                json.dump(users, f, indent=4)

            await message.add_reaction('✅')
            
            embed = discord.Embed(title = "Success Rewards", color = config['embed_color'])
            embed.add_field(name = "Attachments", value = f"You have earned 1 point!")
            embed.add_field(name = "Total Points", value = users[str(message.author.id)], inline=False)
            embed.set_footer(text = config["embed_text"], icon_url=config["embed_icon"])

            await message.reply(embed = embed)

            return
        
        else:
            await message.add_reaction('❌')
            
            embed = discord.Embed(title = "Success Rewards", color = config['embed_color'])
            embed.add_field(name = "Invalid Message", value = f"You have not earned any points.")
            embed.add_field(name = "Total Points", value = users[str(message.author.id)], inline=False)
            embed.set_footer(text = config["embed_text"], icon_url=config["embed_icon"])

            await message.reply(embed = embed)

            return
        
    else:
        pass

@vouch.command(description="Displays information about you or another user!")
async def check(ctx: discord.ApplicationContext, member: discord.Member):
    await ctx.defer()

    with open(os.getcwd() + '/Vouches.json') as f:
        vouches = json.load(f)

    member_id = str(member.id)
    if member_id in vouches:
        vouch_data = vouches[member_id]
        positive_vouches = vouch_data["positive_vouch"]
        negative_vouches = vouch_data["negative_vouch"]
    else:
        positive_vouches = []
        negative_vouches = []

    num_positive_vouches = len(positive_vouches)
    num_negative_vouches = len(negative_vouches)
    total_vouches = num_positive_vouches + num_negative_vouches

    positive_vouches.sort(key=lambda vouch: vouch["timestamp"], reverse=True)
    negative_vouches.sort(key=lambda vouch: vouch["timestamp"], reverse=True)

    last_positive_vouches = positive_vouches[:5]
    last_negative_vouches = negative_vouches[:5]

    positive_vouch_text = "\n".join(
        f"<t:{str(datetime.datetime.fromtimestamp(vouch['timestamp']).timestamp()).split('.')[0]}> - <@{vouch['tag']}>: {vouch['text']}"
        for vouch in last_positive_vouches
    )
    negative_vouch_text = "\n".join(
        f"<t:{str(datetime.datetime.fromtimestamp(vouch['timestamp']).timestamp()).split('.')[0]}> - <@{vouch['tag']}>: {vouch['text']}"
        for vouch in last_negative_vouches
    )

    total_vouches = num_positive_vouches + num_negative_vouches
    if total_vouches > 0:
        user_rating_percentage = (num_positive_vouches / total_vouches) * 100
    else:
        user_rating_percentage = 0

    embed = discord.Embed(title="Vouch Information", description=f"User: {member.mention}", color=config['embed_color'])
    embed.add_field(name="**Member ID**", value=member.id, inline=False)
    embed.add_field(name="Joined Server", value=f'<t:{str(datetime.datetime.strptime(member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S").timestamp()).split(".")[0]}>', inline=False)
    embed.add_field(name="Joined Discord", value=f'<t:{str(datetime.datetime.strptime(member.created_at.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S").timestamp()).split(".")[0]}>', inline=False)
    embed.add_field(name="Total | Positive | Negative", value=f"{str(total_vouches)} | {str(num_positive_vouches)} | {str(num_negative_vouches)}", inline=False)
    embed.add_field(name="User Rating Percentage", value=f"{user_rating_percentage:.2f}%", inline=False)
    embed.add_field(name="Last 5 Positive Vouches", value=positive_vouch_text, inline=False)
    embed.add_field(name="Last 5 Negative Vouches", value=negative_vouch_text, inline=False)
    embed.set_thumbnail(url=member.avatar.url)
    embed.set_footer(text=config["embed_text"], icon_url=config["embed_icon"])

    await ctx.respond(embed=embed)

@vouch.command(description="Vouch for a user!")
@option("vouch", description="Positive or Negative", choices=["Positive", "Negative"])
async def member(ctx: discord.ApplicationContext, member: discord.Member, reason: str, vouch: str):
    await ctx.defer()

    if ctx.author.id != member.id:
        with open(os.getcwd() + '/Vouches.json') as f:
            vouches = json.load(f)

        member_id = str(member.id)
        if member_id in vouches:
            vouch_data = vouches[member_id]
        else:
            vouch_data = {
                "positive_vouch": [],
                "negative_vouch": []
            }

        timestamp = datetime.datetime.now().timestamp()
        vouch_entry = {
            "timestamp": timestamp,
            "tag": ctx.author.id,
            "text": reason
        }
        if vouch.lower() == "positive":
            vouch_data["positive_vouch"].append(vouch_entry)
        elif vouch.lower() == "negative":
            vouch_data["negative_vouch"].append(vouch_entry)

        vouches[member_id] = vouch_data

        with open(os.getcwd() + "/Vouches.json", "w") as f:
            json.dump(vouches, f, indent=4)

        embed = discord.Embed(title=f"{vouch.capitalize()} Vouch",
                              description=f"{member.mention} has been {vouch.lower()}ly vouched by {ctx.author.mention}!",
                              timestamp=datetime.datetime.now(), color=config['embed_color'])
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text=config["embed_text"], icon_url=config["embed_icon"])

        await ctx.respond(embed=embed)
    
    else:
        embed = discord.Embed(title="Invalid Member", description="You cannot vouch for yourself!", color=config['embed_color'])
        embed.set_footer(text=config["embed_text"], icon_url=config["embed_icon"])

        await ctx.respond(embed=embed)


client.run(config['bot_token'])