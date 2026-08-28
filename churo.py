import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio
import datetime
import json
import os

# ==========================================
# CONFIGURATION
# ==========================================
TOKEN = os.getenv('TOKEN')
SUGGESTION_CHANNEL_ID = 1542713625096233012

# ==========================================
# BOT SETUP
# ==========================================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

# ==========================================
# SUGGESTION SYSTEM
# ==========================================
SUGGESTIONS_FILE = 'suggestions.json'

def load_suggestions():
    if os.path.exists(SUGGESTIONS_FILE):
        with open(SUGGESTIONS_FILE, 'r') as f:
            return json.load(f)
    return {"suggestions": [], "suggestion_id": 0}

def save_suggestions(data):
    with open(SUGGESTIONS_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# ==========================================
# BOT READY EVENT
# ==========================================
@bot.event
async def on_ready():
    print(f'✅ {bot.user} has connected to Discord!')
    print(f'📊 Bot is in {len(bot.guilds)} servers')
    await bot.change_presence(activity=discord.Game(name="/help"))
    
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash commands")
        for cmd in synced:
            print(f"   /{cmd.name}")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

# ==========================================
# INFORMATION COMMANDS
# ==========================================

@bot.tree.command(name="ping", description="Check bot latency")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Latency: **{latency}ms**",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="serverinfo", description="Get information about the server")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    
    embed = discord.Embed(
        title=f"📊 {guild.name}",
        description="Server Information",
        color=discord.Color.blue(),
        timestamp=datetime.datetime.now()
    )
    
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    embed.add_field(name="👑 Owner", value=guild.owner.mention, inline=True)
    embed.add_field(name="📅 Created On", value=guild.created_at.strftime("%B %d, %Y"), inline=True)
    embed.add_field(name="👥 Members", value=guild.member_count, inline=True)
    embed.add_field(name="📝 Channels", value=len(guild.channels), inline=True)
    embed.add_field(name="🎭 Roles", value=len(guild.roles), inline=True)
    embed.add_field(name="🚀 Boost Level", value=guild.premium_tier, inline=True)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="userinfo", description="Get information about a user")
@app_commands.describe(member="The user to get information about (optional)")
async def userinfo(interaction: discord.Interaction, member: discord.Member = None):
    if member is None:
        member = interaction.user
    
    embed = discord.Embed(
        title=f"👤 {member.display_name}",
        description="User Information",
        color=member.color,
        timestamp=datetime.datetime.now()
    )
    
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    embed.add_field(name="🆔 ID", value=member.id, inline=True)
    embed.add_field(name="📅 Joined Server", value=member.joined_at.strftime("%B %d, %Y"), inline=True)
    embed.add_field(name="📅 Joined Discord", value=member.created_at.strftime("%B %d, %Y"), inline=True)
    embed.add_field(name="🎭 Roles", value=len(member.roles) - 1, inline=True)
    embed.add_field(name="⭐ Top Role", value=member.top_role.mention, inline=True)
    embed.add_field(name="🤖 Bot", value="Yes" if member.bot else "No", inline=True)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="avatar", description="Get a user's avatar")
@app_commands.describe(member="The user to get the avatar of (optional)")
async def avatar(interaction: discord.Interaction, member: discord.Member = None):
    if member is None:
        member = interaction.user
    
    embed = discord.Embed(
        title=f"{member.display_name}'s Avatar",
        color=member.color
    )
    embed.set_image(url=member.avatar.url if member.avatar else member.default_avatar.url)
    await interaction.response.send_message(embed=embed)

# ==========================================
# FUN COMMANDS
# ==========================================

@bot.tree.command(name="roll", description="Roll a dice (1-6)")
async def roll(interaction: discord.Interaction):
    result = random.randint(1, 6)
    await interaction.response.send_message(f"🎲 {interaction.user.mention} rolled a **{result}**!")

@bot.tree.command(name="flip", description="Flip a coin")
async def flip(interaction: discord.Interaction):
    result = random.choice(["Heads", "Tails"])
    await interaction.response.send_message(f"🪙 {interaction.user.mention} flipped **{result}**!")

@bot.tree.command(name="choose", description="Choose between multiple options")
@app_commands.describe(
    option1="First option",
    option2="Second option",
    option3="Third option (optional)",
    option4="Fourth option (optional)"
)
async def choose(
    interaction: discord.Interaction, 
    option1: str, 
    option2: str, 
    option3: str = None, 
    option4: str = None
):
    options = [option1, option2]
    if option3:
        options.append(option3)
    if option4:
        options.append(option4)
    
    choice = random.choice(options)
    await interaction.response.send_message(f"🤔 I choose: **{choice}**")

@bot.tree.command(name="8ball", description="Ask the magic 8-ball a question")
@app_commands.describe(question="Your question for the magic 8-ball")
async def eightball(interaction: discord.Interaction, question: str):
    responses = [
        "It is certain.", "It is decidedly so.", "Without a doubt.",
        "Yes - definitely.", "You may rely on it.", "As I see it, yes.",
        "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
        "Reply hazy, try again.", "Ask again later.", "Better not tell you now.",
        "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.",
        "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."
    ]
    
    response = random.choice(responses)
    embed = discord.Embed(
        title="🎱 Magic 8-Ball",
        color=discord.Color.purple()
    )
    embed.add_field(name="❓ Question", value=question, inline=False)
    embed.add_field(name="💬 Answer", value=response, inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="password", description="Generate a random password")
@app_commands.describe(length="Password length (4-64)")
async def password(interaction: discord.Interaction, length: int = 12):
    if length < 4 or length > 64:
        await interaction.response.send_message("❌ Password length must be between 4 and 64 characters.", ephemeral=True)
        return
    
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+"
    password = ''.join(random.choice(chars) for _ in range(length))
    
    embed = discord.Embed(
        title="🔐 Generated Password",
        description=f"```{password}```",
        color=discord.Color.gold()
    )
    embed.set_footer(text="Make sure to save this password securely!")
    await interaction.response.send_message(embed=embed)

# ==========================================
# SUGGESTION COMMANDS
# ==========================================

@bot.tree.command(name="suggest", description="Submit a suggestion to the server")
@app_commands.describe(
    suggestion="What would you like to suggest?",
    category="Category of your suggestion"
)
@app_commands.choices(category=[
    app_commands.Choice(name="General", value="general"),
    app_commands.Choice(name="Bot", value="bot"),
    app_commands.Choice(name="Server", value="server"),
    app_commands.Choice(name="Moderation", value="moderation"),
    app_commands.Choice(name="Other", value="other")
])
async def suggest(
    interaction: discord.Interaction, 
    suggestion: str, 
    category: app_commands.Choice[str] = None
):
    if SUGGESTION_CHANNEL_ID is None:
        await interaction.response.send_message(
            "❌ The suggestion system is not configured. Please contact an administrator.",
            ephemeral=True
        )
        return
    
    data = load_suggestions()
    data["suggestion_id"] += 1
    suggestion_id = data["suggestion_id"]
    
    suggestion_data = {
        "id": suggestion_id,
        "author_id": interaction.user.id,
        "author_name": str(interaction.user),
        "author_display": interaction.user.display_name,
        "suggestion": suggestion,
        "category": category.value if category else "general",
        "category_name": category.name if category else "General",
        "timestamp": datetime.datetime.now().isoformat(),
        "status": "pending",
        "votes": {"upvotes": [], "downvotes": []}
    }
    
    data["suggestions"].append(suggestion_data)
    save_suggestions(data)
    
    channel = bot.get_channel(SUGGESTION_CHANNEL_ID)
    if not channel:
        await interaction.response.send_message(
            "❌ Suggestion channel not found. Please contact an administrator.",
            ephemeral=True
        )
        return
    
    embed = discord.Embed(
        title=f"💡 New Suggestion #{suggestion_id}",
        description=suggestion,
        color=discord.Color.blue(),
        timestamp=datetime.datetime.now()
    )
    
    embed.add_field(name="📂 Category", value=category.name if category else "General", inline=True)
    embed.add_field(name="📊 Status", value="🟡 Pending Review", inline=True)
    embed.add_field(name="👍 Votes", value="⬆️ 0 | ⬇️ 0", inline=True)
    embed.set_footer(
        text=f"Suggested by {interaction.user.display_name}",
        icon_url=interaction.user.avatar.url if interaction.user.avatar else None
    )
    
    suggestion_message = await channel.send(embed=embed)
    await suggestion_message.add_reaction("⬆️")
    await suggestion_message.add_reaction("⬇️")
    
    suggestion_data["message_id"] = suggestion_message.id
    save_suggestions(data)
    
    await interaction.response.send_message(
        f"✅ Your suggestion (#{suggestion_id}) has been submitted! Check it out in <#{SUGGESTION_CHANNEL_ID}>",
        ephemeral=True
    )

@bot.tree.command(name="suggest_list", description="View all suggestions")
@app_commands.describe(
    status="Filter by status",
    limit="Number of suggestions to show (max 25)"
)
@app_commands.choices(status=[
    app_commands.Choice(name="All", value="all"),
    app_commands.Choice(name="Pending", value="pending"),
    app_commands.Choice(name="Approved", value="approved"),
    app_commands.Choice(name="Denied", value="denied"),
    app_commands.Choice(name="Implemented", value="implemented")
])
async def suggest_list(
    interaction: discord.Interaction,
    status: app_commands.Choice[str] = None,
    limit: int = 10
):
    if limit > 25:
        limit = 25
    if limit < 1:
        limit = 1
    
    data = load_suggestions()
    suggestions = data["suggestions"]
    
    if status and status.value != "all":
        suggestions = [s for s in suggestions if s["status"] == status.value]
    
    suggestions = sorted(suggestions, key=lambda x: x["id"], reverse=True)
    suggestions = suggestions[:limit]
    
    if not suggestions:
        await interaction.response.send_message("📭 No suggestions found.", ephemeral=True)
        return
    
    status_emojis = {
        "pending": "🟡",
        "approved": "🟢",
        "denied": "🔴",
        "implemented": "💜"
    }
    
    embed = discord.Embed(
        title=f"💡 Suggestions ({len(suggestions)} shown)",
        color=discord.Color.gold(),
        timestamp=datetime.datetime.now()
    )
    
    for s in suggestions[:25]:
        status_emoji = status_emojis.get(s["status"], "🟡")
        votes = len(s["votes"]["upvotes"]) - len(s["votes"]["downvotes"])
        vote_icon = "⬆️" if votes > 0 else "⬇️" if votes < 0 else "➖"
        
        value = f"📝 {s['suggestion'][:100]}"
        if len(s['suggestion']) > 100:
            value += "..."
        value += f"\n📂 {s['category_name']} | {vote_icon} {votes} votes | {status_emoji} {s['status'].title()}"
        
        embed.add_field(
            name=f"#{s['id']} - {s['author_display']}",
            value=value,
            inline=False
        )
    
    embed.set_footer(text=f"Total suggestions: {len(data['suggestions'])}")
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="suggest_view", description="View details of a specific suggestion")
@app_commands.describe(suggestion_id="The ID of the suggestion to view")
async def suggest_view(interaction: discord.Interaction, suggestion_id: int):
    data = load_suggestions()
    
    suggestion = None
    for s in data["suggestions"]:
        if s["id"] == suggestion_id:
            suggestion = s
            break
    
    if not suggestion:
        await interaction.response.send_message(f"❌ Suggestion #{suggestion_id} not found.", ephemeral=True)
        return
    
    status_emojis = {
        "pending": "🟡",
        "approved": "🟢",
        "denied": "🔴",
        "implemented": "💜"
    }
    
    embed = discord.Embed(
        title=f"💡 Suggestion #{suggestion['id']}",
        description=suggestion['suggestion'],
        color=discord.Color.blue(),
        timestamp=datetime.datetime.fromisoformat(suggestion['timestamp'])
    )
    
    embed.add_field(name="👤 Author", value=f"{suggestion['author_display']} ({suggestion['author_name']})", inline=True)
    embed.add_field(name="📂 Category", value=suggestion['category_name'], inline=True)
    embed.add_field(name="📊 Status", value=f"{status_emojis.get(suggestion['status'], '🟡')} {suggestion['status'].title()}", inline=True)
    
    votes = len(suggestion['votes']['upvotes']) - len(suggestion['votes']['downvotes'])
    embed.add_field(
        name="👍 Votes",
        value=f"⬆️ {len(suggestion['votes']['upvotes'])} | ⬇️ {len(suggestion['votes']['downvotes'])} (Net: {votes})",
        inline=True
    )
    
    if suggestion.get('status_reason'):
        embed.add_field(name="📝 Reason", value=suggestion['status_reason'], inline=False)
    
    embed.set_footer(text=f"ID: {suggestion['id']} | Submitted")
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="suggest_stats", description="View suggestion statistics")
async def suggest_stats(interaction: discord.Interaction):
    data = load_suggestions()
    suggestions = data["suggestions"]
    
    if not suggestions:
        await interaction.response.send_message("📭 No suggestions have been submitted yet.", ephemeral=True)
        return
    
    total = len(suggestions)
    pending = len([s for s in suggestions if s["status"] == "pending"])
    approved = len([s for s in suggestions if s["status"] == "approved"])
    denied = len([s for s in suggestions if s["status"] == "denied"])
    implemented = len([s for s in suggestions if s["status"] == "implemented"])
    
    user_suggestions = {}
    for s in suggestions:
        user_id = s["author_id"]
        if user_id not in user_suggestions:
            user_suggestions[user_id] = {"name": s["author_display"], "count": 0}
        user_suggestions[user_id]["count"] += 1
    
    top_users = sorted(user_suggestions.items(), key=lambda x: x[1]["count"], reverse=True)[:3]
    top_users_text = "\n".join([f"{u[1]['name']}: {u[1]['count']} suggestions" for u in top_users]) if top_users else "None"
    
    embed = discord.Embed(
        title="📊 Suggestion Statistics",
        color=discord.Color.green(),
        timestamp=datetime.datetime.now()
    )
    
    embed.add_field(name="📝 Total Suggestions", value=str(total), inline=True)
    embed.add_field(name="🟡 Pending", value=str(pending), inline=True)
    embed.add_field(name="🟢 Approved", value=str(approved), inline=True)
    embed.add_field(name="🔴 Denied", value=str(denied), inline=True)
    embed.add_field(name="💜 Implemented", value=str(implemented), inline=True)
    embed.add_field(name="✅ Approval Rate", value=f"{round((approved + implemented) / total * 100, 1)}%" if total > 0 else "0%", inline=True)
    embed.add_field(name="🏆 Top Suggesters", value=top_users_text, inline=False)
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

# ==========================================
# MODERATION COMMANDS
# ==========================================

@bot.tree.command(name="clear", description="Delete messages in a channel")
@app_commands.describe(amount="Number of messages to delete (1-100)")
@app_commands.default_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, amount: int = 5):
    if amount <= 0 or amount > 100:
        await interaction.response.send_message("❌ Please specify between 1-100 messages.", ephemeral=True)
        return
    
    await interaction.response.defer(ephemeral=True)
    deleted = await interaction.channel.purge(limit=amount)
    
    await interaction.followup.send(f"✅ Deleted {len(deleted)} messages.", ephemeral=True)

@bot.tree.command(name="kick", description="Kick a member from the server")
@app_commands.describe(
    member="The member to kick",
    reason="Reason for the kick (optional)"
)
@app_commands.default_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    if member == interaction.user:
        await interaction.response.send_message("❌ You can't kick yourself!", ephemeral=True)
        return
    if member == interaction.guild.owner:
        await interaction.response.send_message("❌ You can't kick the server owner!", ephemeral=True)
        return
    if member.top_role >= interaction.user.top_role and interaction.user != interaction.guild.owner:
        await interaction.response.send_message("❌ You can't kick someone with a higher or equal role!", ephemeral=True)
        return
    
    try:
        await member.kick(reason=reason)
        embed = discord.Embed(
            title="Member Kicked",
            description=f"✅ {member.mention} has been kicked.",
            color=discord.Color.red()
        )
        embed.add_field(name="Reason", value=reason)
        embed.add_field(name="Moderator", value=interaction.user.mention)
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to kick that member.", ephemeral=True)

@bot.tree.command(name="ban", description="Ban a member from the server")
@app_commands.describe(
    member="The member to ban",
    reason="Reason for the ban (optional)"
)
@app_commands.default_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    if member == interaction.user:
        await interaction.response.send_message("❌ You can't ban yourself!", ephemeral=True)
        return
    if member == interaction.guild.owner:
        await interaction.response.send_message("❌ You can't ban the server owner!", ephemeral=True)
        return
    if member.top_role >= interaction.user.top_role and interaction.user != interaction.guild.owner:
        await interaction.response.send_message("❌ You can't ban someone with a higher or equal role!", ephemeral=True)
        return
    
    try:
        await member.ban(reason=reason)
        embed = discord.Embed(
            title="Member Banned",
            description=f"✅ {member.mention} has been banned.",
            color=discord.Color.dark_red()
        )
        embed.add_field(name="Reason", value=reason)
        embed.add_field(name="Moderator", value=interaction.user.mention)
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to ban that member.", ephemeral=True)

@bot.tree.command(name="unban", description="Unban a user from the server")
@app_commands.describe(user_id="The ID of the user to unban")
@app_commands.default_permissions(ban_members=True)
async def unban(interaction: discord.Interaction, user_id: str):
    try:
        user = await bot.fetch_user(int(user_id))
        await interaction.guild.unban(user)
        await interaction.response.send_message(f"✅ Unbanned {user.mention}")
    except discord.NotFound:
        await interaction.response.send_message(f"❌ User ID {user_id} not found or not banned.", ephemeral=True)
    except ValueError:
        await interaction.response.send_message("❌ Please provide a valid user ID.", ephemeral=True)

@bot.tree.command(name="slowmode", description="Set slowmode in the current channel")
@app_commands.describe(seconds="Slowmode in seconds (0 to disable)")
@app_commands.default_permissions(manage_channels=True)
async def slowmode(interaction: discord.Interaction, seconds: int = 0):
    if seconds < 0:
        await interaction.response.send_message("❌ Please enter a positive number.", ephemeral=True)
        return
    if seconds > 21600:
        await interaction.response.send_message("❌ Slowmode cannot exceed 21600 seconds (6 hours).", ephemeral=True)
        return
    
    try:
        await interaction.channel.edit(slowmode_delay=seconds)
        if seconds == 0:
            await interaction.response.send_message("✅ Slowmode has been disabled.")
        else:
            await interaction.response.send_message(f"✅ Slowmode set to {seconds} seconds.")
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to change slowmode.", ephemeral=True)

@bot.tree.command(name="mute", description="Mute a member in voice chat")
@app_commands.describe(member="The member to mute")
@app_commands.default_permissions(mute_members=True)
async def mute(interaction: discord.Interaction, member: discord.Member):
    if not member.voice:
        await interaction.response.send_message("❌ That member is not in a voice channel.", ephemeral=True)
        return
    
    try:
        await member.edit(mute=True)
        await interaction.response.send_message(f"🔇 {member.mention} has been muted in voice chat.")
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to mute that member.", ephemeral=True)

@bot.tree.command(name="unmute", description="Unmute a member in voice chat")
@app_commands.describe(member="The member to unmute")
@app_commands.default_permissions(mute_members=True)
async def unmute(interaction: discord.Interaction, member: discord.Member):
    if not member.voice:
        await interaction.response.send_message("❌ That member is not in a voice channel.", ephemeral=True)
        return
    
    try:
        await member.edit(mute=False)
        await interaction.response.send_message(f"🔊 {member.mention} has been unmuted in voice chat.")
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to unmute that member.", ephemeral=True)

@bot.tree.command(name="suggest_status", description="Change the status of a suggestion (Moderator only)")
@app_commands.describe(
    suggestion_id="The ID of the suggestion",
    status="New status for the suggestion",
    reason="Reason for the status change (optional)"
)
@app_commands.choices(status=[
    app_commands.Choice(name="Approved", value="approved"),
    app_commands.Choice(name="Denied", value="denied"),
    app_commands.Choice(name="Implemented", value="implemented")
])
@app_commands.default_permissions(manage_messages=True)
async def suggest_status(
    interaction: discord.Interaction, 
    suggestion_id: int,
    status: app_commands.Choice[str],
    reason: str = None
):
    data = load_suggestions()
    
    suggestion = None
    for s in data["suggestions"]:
        if s["id"] == suggestion_id:
            suggestion = s
            break
    
    if not suggestion:
        await interaction.response.send_message(f"❌ Suggestion #{suggestion_id} not found.", ephemeral=True)
        return
    
    suggestion["status"] = status.value
    suggestion["status_reason"] = reason
    suggestion["status_updated_by"] = str(interaction.user)
    suggestion["status_updated_at"] = datetime.datetime.now().isoformat()
    save_suggestions(data)
    
    status_emojis = {
        "pending": "🟡",
        "approved": "🟢",
        "denied": "🔴",
        "implemented": "💜"
    }
    
    status_labels = {
        "pending": "Pending Review",
        "approved": "✅ Approved",
        "denied": "❌ Denied",
        "implemented": "💜 Implemented"
    }
    
    if "message_id" in suggestion:
        try:
            channel = bot.get_channel(SUGGESTION_CHANNEL_ID)
            if channel:
                message = await channel.fetch_message(suggestion["message_id"])
                if message and message.embeds:
                    embed = message.embeds[0].to_dict()
                    status_value = f"{status_emojis.get(status.value, '')} {status_labels.get(status.value, status.value)}"
                    embed["fields"][1]["value"] = status_value
                    if reason:
                        embed["fields"][2]["value"] = f"⬆️ {len(suggestion['votes']['upvotes'])} | ⬇️ {len(suggestion['votes']['downvotes'])}\n\n**Reason:** {reason}"
                    await message.edit(embed=discord.Embed.from_dict(embed))
        except:
            pass
    
    await interaction.response.send_message(
        f"✅ Suggestion #{suggestion_id} status updated to **{status.value.title()}**!",
        ephemeral=True
    )

@bot.tree.command(name="suggest_purge", description="Delete a suggestion (Admin only)")
@app_commands.describe(suggestion_id="The ID of the suggestion to delete")
@app_commands.default_permissions(administrator=True)
async def suggest_purge(interaction: discord.Interaction, suggestion_id: int):
    data = load_suggestions()
    
    suggestion = None
    for i, s in enumerate(data["suggestions"]):
        if s["id"] == suggestion_id:
            suggestion = s
            index = i
            break
    
    if not suggestion:
        await interaction.response.send_message(f"❌ Suggestion #{suggestion_id} not found.", ephemeral=True)
        return
    
    if "message_id" in suggestion:
        try:
            channel = bot.get_channel(SUGGESTION_CHANNEL_ID)
            if channel:
                message = await channel.fetch_message(suggestion["message_id"])
                await message.delete()
        except:
            pass
    
    data["suggestions"].pop(index)
    save_suggestions(data)
    
    await interaction.response.send_message(f"✅ Suggestion #{suggestion_id} has been deleted.", ephemeral=True)

# ==========================================
# HELP COMMAND
# ==========================================

@bot.tree.command(name="help", description="Show all available commands")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🤖 Elchuro Bot Commands",
        description="Here are all available slash commands:",
        color=discord.Color.green(),
        timestamp=datetime.datetime.now()
    )
    
    categories = {
        "📊 Information": [
            "/ping - Check bot latency",
            "/serverinfo - Get server information",
            "/userinfo - Get user information",
            "/avatar - Get a user's avatar"
        ],
        "🎮 Fun": [
            "/roll - Roll a dice",
            "/flip - Flip a coin",
            "/choose - Choose between options",
            "/8ball - Ask the magic 8-ball",
            "/password - Generate a random password"
        ],
        "💡 Suggestions": [
            "/suggest - Submit a suggestion",
            "/suggest_list - View all suggestions",
            "/suggest_view - View a specific suggestion",
            "/suggest_stats - View suggestion statistics"
        ],
        "⚙️ Moderation": [
            "/clear - Delete messages",
            "/kick - Kick a member",
            "/ban - Ban a member",
            "/unban - Unban a user",
            "/mute - Mute in voice chat",
            "/unmute - Unmute in voice chat",
            "/slowmode - Set slowmode"
        ],
        "🔧 Admin": [
            "/suggest_status - Change suggestion status",
            "/suggest_purge - Delete a suggestion"
        ]
    }
    
    for category, commands_list in categories.items():
        command_string = "\n".join(commands_list)
        embed.add_field(name=category, value=command_string, inline=False)
    
    embed.set_footer(text="Use /suggest to submit suggestions!")
    await interaction.response.send_message(embed=embed)

# ==========================================
# VOTING SYSTEM
# ==========================================

@bot.event
async def on_raw_reaction_add(payload):
    if payload.channel_id != SUGGESTION_CHANNEL_ID:
        return
    if payload.user_id == bot.user.id:
        return
    
    data = load_suggestions()
    
    suggestion = None
    for s in data["suggestions"]:
        if s.get("message_id") == payload.message_id:
            suggestion = s
            break
    
    if not suggestion:
        return
    
    user_id = payload.user_id
    emoji = str(payload.emoji)
    
    if emoji == "⬆️":
        if user_id in suggestion["votes"]["downvotes"]:
            suggestion["votes"]["downvotes"].remove(user_id)
        if user_id not in suggestion["votes"]["upvotes"]:
            suggestion["votes"]["upvotes"].append(user_id)
    elif emoji == "⬇️":
        if user_id in suggestion["votes"]["upvotes"]:
            suggestion["votes"]["upvotes"].remove(user_id)
        if user_id not in suggestion["votes"]["downvotes"]:
            suggestion["votes"]["downvotes"].append(user_id)
    
    save_suggestions(data)
    
    try:
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        if message and message.embeds:
            embed = message.embeds[0].to_dict()
            embed["fields"][2]["value"] = f"⬆️ {len(suggestion['votes']['upvotes'])} | ⬇️ {len(suggestion['votes']['downvotes'])}"
            await message.edit(embed=discord.Embed.from_dict(embed))
    except:
        pass

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.channel_id != SUGGESTION_CHANNEL_ID:
        return
    
    data = load_suggestions()
    
    suggestion = None
    for s in data["suggestions"]:
        if s.get("message_id") == payload.message_id:
            suggestion = s
            break
    
    if not suggestion:
        return
    
    user_id = payload.user_id
    emoji = str(payload.emoji)
    
    if emoji == "⬆️" and user_id in suggestion["votes"]["upvotes"]:
        suggestion["votes"]["upvotes"].remove(user_id)
    elif emoji == "⬇️" and user_id in suggestion["votes"]["downvotes"]:
        suggestion["votes"]["downvotes"].remove(user_id)
    
    save_suggestions(data)
    
    try:
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        if message and message.embeds:
            embed = message.embeds[0].to_dict()
            embed["fields"][2]["value"] = f"⬆️ {len(suggestion['votes']['upvotes'])} | ⬇️ {len(suggestion['votes']['downvotes'])}"
            await message.edit(embed=discord.Embed.from_dict(embed))
    except:
        pass

# ==========================================
# RUN THE BOT
# ==========================================

if __name__ == "__main__":
    bot.run(TOKEN)