import discord, json, os

with open(os.getcwd() + '/Config.json') as f:
    config = json.load(f)

intents = discord.Intents().all()
intents.message_content = True
client = discord.Bot(intents=intents)


@client.event
async def on_ready():
    print("Bot is ready!")

users = {}

with open(os.getcwd() + "/Points.json") as f:
    users = json.load(f)

@client.slash_command(description = "Get Points")
async def points(ctx: discord.ApplicationContext, user: discord.Member):
    with open(os.getcwd() + '/Points.json') as f:
        users = json.load(f)
    
    for user in users:
        if user == str(user.id):
            await ctx.respond(f"{user.mention} has {users[user]} points!")
            return
    
    await ctx.respond(f"{user.mention} has 0 points!")

@client.event
async def on_message(message):
    if message.channel.id == config['channel_id'] and message.author.id != client.user.id:
        if 'https://twitter.com' in message.content:
            if str(message.author.id) in users:
                users[str(message.author.id)] += 5
            else:
                users[str(message.author.id)] = 5
            
            with open(os.getcwd() + "/Points.json", "w") as f:
                json.dump(users, f, indent=4)

            await message.add_reaction('✅')
            await message.reply(f"Congratulations {message.author.mention}! You have earned 5 points!")

            return
    
        elif message.attachments:
            if str(message.author.id) in users:
                users[str(message.author.id)] += 1
            else:
                users[str(message.author.id)] = 1

            with open(os.getcwd() + "/Points.json", "w") as f:
                json.dump(users, f, indent=4)

            await message.add_reaction('✅')
            await message.reply(f"Congratulations {message.author.mention}! You have earned 1 point!")

            return
        
        else:
            await message.add_reaction('❌')
            await message.reply(f"Sorry {message.author.mention}, you have not earned any points!")

            return
        
    else:
        pass

client.run(config['bot_token'])