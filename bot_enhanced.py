"""
Guardify - Advanced Discord Moderation Bot
AI-enabled bot with comprehensive moderation features and user-friendly interface
"""

import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from datetime import datetime, timedelta
from textblob import TextBlob
import re
from typing import Dict, List, Optional
import asyncio
from collections import defaultdict


class AbuseDetector:
    """Advanced abuse detection with ML-based sentiment analysis."""
    
    SENTIMENT_THRESHOLD = -0.3
    KEYWORD_WEIGHT = 0.4
    ABUSE_SCORE_THRESHOLD = 0.4
    
    def __init__(self):
        self.abusive_keywords = [
            'hate', 'kill', 'stupid', 'idiot', 'loser', 'trash',
            'worthless', 'pathetic', 'disgusting', 'die', 'kys',
            'retard', 'moron', 'dumb', 'ugly', 'fat', 'nazi',
            'fuck', 'shit', 'bitch', 'ass', 'damn'
        ]
        self.spam_tracker = defaultdict(list)
        
    def analyze_message(self, content: str) -> Dict:
        """Analyze message for abusive content."""
        content_lower = content.lower()
        
        blob = TextBlob(content)
        sentiment = blob.sentiment.polarity
        
        detected_keywords = []
        for keyword in self.abusive_keywords:
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, content_lower):
                detected_keywords.append(keyword)
        
        keyword_score = len(detected_keywords) * self.KEYWORD_WEIGHT
        sentiment_score = abs(min(sentiment, 0))
        abuse_score = keyword_score + sentiment_score
        
        is_abusive = abuse_score > self.ABUSE_SCORE_THRESHOLD or sentiment < self.SENTIMENT_THRESHOLD
        
        severity = "low"
        if abuse_score > 0.8:
            severity = "high"
        elif abuse_score > 0.5:
            severity = "medium"
        
        return {
            "is_abusive": is_abusive,
            "abuse_score": round(abuse_score, 3),
            "sentiment": round(sentiment, 3),
            "detected_keywords": detected_keywords,
            "severity": severity,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def check_spam(self, user_id: int, message_time: datetime) -> bool:
        """Check if user is spamming."""
        self.spam_tracker[user_id].append(message_time)
        
        # Keep only messages from last 5 seconds
        cutoff = message_time - timedelta(seconds=5)
        self.spam_tracker[user_id] = [t for t in self.spam_tracker[user_id] if t > cutoff]
        
        # If more than 5 messages in 5 seconds, it's spam
        return len(self.spam_tracker[user_id]) > 5


class ForensicsLogger:
    """Enhanced forensics logging with CSV export."""
    
    def __init__(self, log_dir: str = "forensics_logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(log_dir, "abuse_evidence.jsonl")
        self.warnings_file = os.path.join(log_dir, "warnings.json")
        self.load_warnings()
        
    def load_warnings(self):
        """Load warning counts from file."""
        if os.path.exists(self.warnings_file):
            with open(self.warnings_file, 'r') as f:
                self.warnings = json.load(f)
        else:
            self.warnings = {}
    
    def save_warnings(self):
        """Save warning counts to file."""
        with open(self.warnings_file, 'w') as f:
            json.dump(self.warnings, f, indent=2)
    
    def add_warning(self, user_id: str, guild_id: str, reason: str) -> int:
        """Add a warning for a user."""
        key = f"{guild_id}:{user_id}"
        if key not in self.warnings:
            self.warnings[key] = []
        
        self.warnings[key].append({
            "reason": reason,
            "timestamp": datetime.utcnow().isoformat()
        })
        self.save_warnings()
        return len(self.warnings[key])
    
    def get_warnings(self, user_id: str, guild_id: str) -> List[Dict]:
        """Get warnings for a user."""
        key = f"{guild_id}:{user_id}"
        return self.warnings.get(key, [])
    
    def remove_warning(self, user_id: str, guild_id: str, index: int) -> bool:
        """Remove a specific warning by index."""
        key = f"{guild_id}:{user_id}"
        if key in self.warnings and 0 <= index < len(self.warnings[key]):
            self.warnings[key].pop(index)
            if len(self.warnings[key]) == 0:
                del self.warnings[key]
            self.save_warnings()
            return True
        return False
    
    def clear_warnings(self, user_id: str, guild_id: str):
        """Clear warnings for a user."""
        key = f"{guild_id}:{user_id}"
        if key in self.warnings:
            del self.warnings[key]
            self.save_warnings()
        
    def log_evidence(self, message: discord.Message, analysis: Dict) -> None:
        """Log evidence of abusive message."""
        evidence = {
            "message_id": str(message.id),
            "author_id": str(message.author.id),
            "author_name": str(message.author),
            "channel_id": str(message.channel.id),
            "channel_name": str(message.channel) if hasattr(message.channel, 'name') else "DM",
            "guild_id": str(message.guild.id) if message.guild else None,
            "guild_name": str(message.guild.name) if message.guild else None,
            "content": message.content,
            "created_at": message.created_at.isoformat(),
            "analysis": analysis,
            "logged_at": datetime.utcnow().isoformat()
        }
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(evidence, ensure_ascii=False) + '\n')
    
    def get_user_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Retrieve abuse history for a specific user."""
        if not os.path.exists(self.log_file):
            return []
        
        records = []
        with open(self.log_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    record = json.loads(line)
                    if record.get('author_id') == user_id:
                        records.append(record)
                        if len(records) >= limit:
                            break
                except json.JSONDecodeError:
                    continue
        
        return records
    
    def get_statistics(self) -> Dict:
        """Get statistics about logged abuse cases."""
        if not os.path.exists(self.log_file):
            return {"total_cases": 0}
        
        stats = {
            "total_cases": 0,
            "severity_breakdown": {"low": 0, "medium": 0, "high": 0},
            "unique_users": set(),
            "unique_guilds": set()
        }
        
        with open(self.log_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    record = json.loads(line)
                    stats["total_cases"] += 1
                    
                    severity = record.get("analysis", {}).get("severity", "low")
                    stats["severity_breakdown"][severity] = stats["severity_breakdown"].get(severity, 0) + 1
                    
                    stats["unique_users"].add(record.get("author_id"))
                    if record.get("guild_id"):
                        stats["unique_guilds"].add(record.get("guild_id"))
                except json.JSONDecodeError:
                    continue
        
        stats["unique_users"] = len(stats["unique_users"])
        stats["unique_guilds"] = len(stats["unique_guilds"])
        
        return stats


class Guardify(commands.Bot):
    """Main bot class with enhanced moderation features."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.abuse_detector = AbuseDetector()
        self.forensics_logger = ForensicsLogger()
        self.auto_mod_enabled = {}  # Guild-specific auto-mod settings
        
    async def setup_hook(self):
        """Setup hook for slash commands."""
        try:
            synced = await self.tree.sync()
            print(f"✅ Synced {len(synced)} slash commands")
        except Exception as e:
            print(f"❌ Failed to sync commands: {e}")
        
    async def on_ready(self):
        """Called when the bot is ready."""
        print(f'╔════════════════════════════════════════╗')
        print(f'║   🛡️  GUARDIFY BOT ONLINE 🛡️           ║')
        print(f'╠════════════════════════════════════════╣')
        print(f'║  Bot: {self.user.name:<28} ║')
        print(f'║  ID: {str(self.user.id):<29} ║')
        print(f'║  Servers: {len(self.guilds):<27} ║')
        print(f'╚════════════════════════════════════════╝')
        
        # Set bot status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="for abuse | !help"
            )
        )
        
    async def on_guild_join(self, guild):
        """Send welcome message when bot joins a server."""
        # Find the first text channel bot can send messages in
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                embed = discord.Embed(
                    title="🛡️ Thanks for adding Guardify!",
                    description="I'm here to keep your server safe and friendly.",
                    color=discord.Color.blue()
                )
                embed.add_field(
                    name="🚀 Getting Started",
                    value="• Use `/help` to see all commands\n"
                          "• I automatically detect abusive messages\n"
                          "• Use `/automod enable` to activate auto-moderation",
                    inline=False
                )
                embed.add_field(
                    name="🔧 Setup Permissions",
                    value="Make sure I have these permissions:\n"
                          "• Manage Messages (to delete abusive content)\n"
                          "• Kick Members (for moderation actions)\n"
                          "• Ban Members (for severe violations)\n"
                          "• Timeout Members (to mute users)",
                    inline=False
                )
                embed.set_footer(text="Need help? Use /support")
                
                try:
                    await channel.send(embed=embed)
                except:
                    pass
                break
        
    async def on_message(self, message: discord.Message):
        """Process every message for abuse detection."""
        if message.author == self.user or message.author.bot:
            return
        
        # Check for spam
        if message.guild and self.abuse_detector.check_spam(message.author.id, message.created_at):
            if self.auto_mod_enabled.get(message.guild.id, False):
                try:
                    await message.delete()
                    await message.channel.send(
                        f"⚠️ {message.author.mention}, please slow down! (Spam detected)",
                        delete_after=5
                    )
                except:
                    pass
        
        # Analyze message
        analysis = self.abuse_detector.analyze_message(message.content)
        
        # Log and handle if abusive
        if analysis['is_abusive']:
            self.forensics_logger.log_evidence(message, analysis)
            
            # Auto-moderation if enabled
            if message.guild and self.auto_mod_enabled.get(message.guild.id, False):
                await self.handle_abusive_message(message, analysis)
        
        await self.process_commands(message)
    
    async def handle_abusive_message(self, message: discord.Message, analysis: Dict):
        """Handle abusive message with appropriate action."""
        try:
            # Delete the message
            await message.delete()
            
            # Add warning
            warning_count = self.forensics_logger.add_warning(
                str(message.author.id),
                str(message.guild.id),
                f"Abusive language (Severity: {analysis['severity']})"
            )
            
            # Create warning embed
            embed = discord.Embed(
                title="⚠️ Warning Issued",
                description=f"{message.author.mention}, your message was removed for violating server rules.",
                color=discord.Color.orange()
            )
            embed.add_field(name="Reason", value="Abusive/Inappropriate Language", inline=False)
            embed.add_field(name="Warnings", value=f"{warning_count}/3", inline=True)
            embed.add_field(name="Severity", value=analysis['severity'].upper(), inline=True)
            
            # Take action based on warning count
            if warning_count >= 3:
                try:
                    await message.author.timeout(timedelta(hours=1), reason="3 warnings for abusive behavior")
                    embed.add_field(name="Action", value="⏱️ Timed out for 1 hour", inline=False)
                except:
                    pass
            elif warning_count >= 2:
                embed.set_footer(text="⚠️ Next warning will result in a timeout")
            
            await message.channel.send(embed=embed, delete_after=10)
            
        except Exception as e:
            print(f"Error handling abusive message: {e}")


# Setup bot
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True

bot = Guardify(command_prefix='!', intents=intents)


# ============= MODERATION COMMANDS =============

@bot.hybrid_command(name='warn', description='Warn a user for violating rules')
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason: str = "No reason provided"):
    """Warn a user."""
    if member.bot:
        await ctx.send("❌ Cannot warn bots!", ephemeral=True)
        return
    
    warning_count = bot.forensics_logger.add_warning(
        str(member.id),
        str(ctx.guild.id),
        reason
    )
    
    embed = discord.Embed(
        title="⚠️ User Warned",
        color=discord.Color.orange(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="User", value=member.mention, inline=True)
    embed.add_field(name="Warned by", value=ctx.author.mention, inline=True)
    embed.add_field(name="Total Warnings", value=f"{warning_count}/3", inline=True)
    embed.add_field(name="Reason", value=reason, inline=False)
    
    await ctx.send(embed=embed)
    
    # Try to DM the user
    try:
        dm_embed = discord.Embed(
            title=f"⚠️ Warning from {ctx.guild.name}",
            description=f"You have been warned by a moderator.",
            color=discord.Color.orange()
        )
        dm_embed.add_field(name="Reason", value=reason)
        dm_embed.add_field(name="Warnings", value=f"{warning_count}/3")
        await member.send(embed=dm_embed)
    except:
        pass


@bot.hybrid_command(name='warnings', description='View warnings for a user')
@commands.has_permissions(manage_messages=True)
async def warnings(ctx, member: discord.Member):
    """View warnings for a user."""
    warns = bot.forensics_logger.get_warnings(str(member.id), str(ctx.guild.id))
    
    embed = discord.Embed(
        title=f"⚠️ Warnings for {member.name}",
        color=discord.Color.orange()
    )
    
    if not warns:
        embed.description = "No warnings found."
    else:
        embed.description = f"Total warnings: {len(warns)}"
        for i, warn in enumerate(warns[-5:], 1):
            embed.add_field(
                name=f"Warning #{i}",
                value=f"**Reason:** {warn['reason']}\n**Date:** {warn['timestamp'][:10]}",
                inline=False
            )
    
    await ctx.send(embed=embed)


@bot.hybrid_command(name='removewarn', description='Remove a specific warning from a user')
@commands.has_permissions(manage_messages=True)
async def removewarn(ctx, member: discord.Member, warning_number: int):
    """Remove a specific warning by number (1-based index)."""
    warns = bot.forensics_logger.get_warnings(str(member.id), str(ctx.guild.id))
    
    if not warns:
        await ctx.send(f"❌ {member.mention} has no warnings!", ephemeral=True)
        return
    
    if warning_number < 1 or warning_number > len(warns):
        await ctx.send(f"❌ Invalid warning number! {member.mention} has {len(warns)} warning(s).", ephemeral=True)
        return
    
    # Remove warning (convert to 0-based index)
    success = bot.forensics_logger.remove_warning(str(member.id), str(ctx.guild.id), warning_number - 1)
    
    if success:
        remaining = len(bot.forensics_logger.get_warnings(str(member.id), str(ctx.guild.id)))
        embed = discord.Embed(
            title="✅ Warning Removed",
            description=f"Removed warning #{warning_number} from {member.mention}\nRemaining warnings: {remaining}",
            color=discord.Color.green(),
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text=f"Removed by {ctx.author}")
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"❌ Failed to remove warning!", ephemeral=True)


@bot.hybrid_command(name='clearwarnings', description='Clear all warnings for a user')
@commands.has_permissions(administrator=True)
async def clearwarnings(ctx, member: discord.Member):
    """Clear warnings for a user."""
    bot.forensics_logger.clear_warnings(str(member.id), str(ctx.guild.id))
    
    embed = discord.Embed(
        title="✅ Warnings Cleared",
        description=f"All warnings have been cleared for {member.mention}",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)


@bot.hybrid_command(name='kick', description='Kick a user from the server')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason: str = "No reason provided"):
    """Kick a user."""
    if member.top_role >= ctx.author.top_role:
        await ctx.send("❌ You cannot kick this user!", ephemeral=True)
        return
    
    embed = discord.Embed(
        title="👢 User Kicked",
        color=discord.Color.red(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="User", value=f"{member.mention} ({member})", inline=True)
    embed.add_field(name="Kicked by", value=ctx.author.mention, inline=True)
    embed.add_field(name="Reason", value=reason, inline=False)
    
    try:
        # Try to DM user
        dm_embed = discord.Embed(
            title=f"Kicked from {ctx.guild.name}",
            description=f"You have been kicked by a moderator.",
            color=discord.Color.red()
        )
        dm_embed.add_field(name="Reason", value=reason)
        await member.send(embed=dm_embed)
    except:
        pass
    
    await member.kick(reason=reason)
    await ctx.send(embed=embed)


@bot.hybrid_command(name='ban', description='Ban a user from the server')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason: str = "No reason provided"):
    """Ban a user."""
    if member.top_role >= ctx.author.top_role:
        await ctx.send("❌ You cannot ban this user!", ephemeral=True)
        return
    
    embed = discord.Embed(
        title="🔨 User Banned",
        color=discord.Color.dark_red(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="User", value=f"{member.mention} ({member})", inline=True)
    embed.add_field(name="Banned by", value=ctx.author.mention, inline=True)
    embed.add_field(name="Reason", value=reason, inline=False)
    
    try:
        dm_embed = discord.Embed(
            title=f"Banned from {ctx.guild.name}",
            description=f"You have been permanently banned.",
            color=discord.Color.dark_red()
        )
        dm_embed.add_field(name="Reason", value=reason)
        await member.send(embed=dm_embed)
    except:
        pass
    
    await member.ban(reason=reason, delete_message_days=1)
    await ctx.send(embed=embed)


@bot.hybrid_command(name='timeout', description='Timeout a user')
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, duration: int, *, reason: str = "No reason provided"):
    """Timeout a user (duration in minutes)."""
    if member.top_role >= ctx.author.top_role:
        await ctx.send("❌ You cannot timeout this user!", ephemeral=True)
        return
    
    await member.timeout(timedelta(minutes=duration), reason=reason)
    
    embed = discord.Embed(
        title="⏱️ User Timed Out",
        color=discord.Color.orange(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="User", value=member.mention, inline=True)
    embed.add_field(name="Duration", value=f"{duration} minutes", inline=True)
    embed.add_field(name="Reason", value=reason, inline=False)
    
    await ctx.send(embed=embed)


@bot.hybrid_command(name='purge', description='Delete multiple messages')
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    """Delete multiple messages."""
    if amount < 1 or amount > 100:
        await ctx.send("❌ Please specify a number between 1 and 100!", ephemeral=True)
        return
    
    deleted = await ctx.channel.purge(limit=amount + 1)
    
    embed = discord.Embed(
        title="🗑️ Messages Deleted",
        description=f"Deleted {len(deleted)-1} messages",
        color=discord.Color.green()
    )
    msg = await ctx.send(embed=embed)
    await asyncio.sleep(3)
    await msg.delete()


# ============= ABUSE DETECTION COMMANDS =============

@bot.hybrid_command(name='scan', description='Scan a message for abusive content')
@commands.has_permissions(manage_messages=True)
async def scan(ctx, *, text: str):
    """Manually scan a message."""
    analysis = bot.abuse_detector.analyze_message(text)
    
    embed = discord.Embed(
        title="🔍 Abuse Detection Analysis",
        color=discord.Color.red() if analysis['is_abusive'] else discord.Color.green()
    )
    
    embed.add_field(name="Abusive", value="✅ Yes" if analysis['is_abusive'] else "❌ No", inline=True)
    embed.add_field(name="Severity", value=analysis['severity'].upper(), inline=True)
    embed.add_field(name="Score", value=f"{analysis['abuse_score']}/1.0", inline=True)
    embed.add_field(name="Sentiment", value=str(analysis['sentiment']), inline=True)
    
    if analysis['detected_keywords']:
        embed.add_field(
            name="Detected Keywords",
            value=", ".join(analysis['detected_keywords']),
            inline=False
        )
    
    await ctx.send(embed=embed)


@bot.hybrid_command(name='history', description='View abuse history for a user')
@commands.has_permissions(manage_messages=True)
async def history(ctx, user: discord.User, limit: int = 5):
    """View abuse history for a user."""
    records = bot.forensics_logger.get_user_history(str(user.id), limit)
    
    if not records:
        embed = discord.Embed(
            title="📋 Clean Record",
            description=f"{user.mention} has no abuse records",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
        return
    
    embed = discord.Embed(
        title=f"📋 Abuse History - {user.name}",
        description=f"Showing {len(records)} most recent cases",
        color=discord.Color.orange()
    )
    
    for i, record in enumerate(records[:limit], 1):
        analysis = record.get('analysis', {})
        embed.add_field(
            name=f"Case #{i} - {analysis.get('severity', 'N/A').upper()}",
            value=f"**Message:** {record.get('content', 'N/A')[:100]}...\n"
                  f"**Score:** {analysis.get('abuse_score', 'N/A')}\n"
                  f"**Date:** {record.get('created_at', 'N/A')[:10]}",
            inline=False
        )
    
    await ctx.send(embed=embed)


@bot.hybrid_command(name='stats', description='View moderation statistics')
@commands.has_permissions(manage_messages=True)
async def stats(ctx):
    """View statistics."""
    stats = bot.forensics_logger.get_statistics()
    
    embed = discord.Embed(
        title="📊 Guardify Statistics",
        color=discord.Color.blue(),
        timestamp=datetime.utcnow()
    )
    
    embed.add_field(name="📝 Total Cases", value=str(stats.get('total_cases', 0)), inline=True)
    embed.add_field(name="👥 Unique Users", value=str(stats.get('unique_users', 0)), inline=True)
    embed.add_field(name="🏰 Servers", value=str(stats.get('unique_guilds', 0)), inline=True)
    
    severity = stats.get('severity_breakdown', {})
    embed.add_field(
        name="⚠️ Severity Breakdown",
        value=f"🟢 Low: {severity.get('low', 0)}\n"
              f"🟡 Medium: {severity.get('medium', 0)}\n"
              f"🔴 High: {severity.get('high', 0)}",
        inline=False
    )
    
    await ctx.send(embed=embed)


@bot.hybrid_command(name='automod', description='Enable/disable auto-moderation')
@commands.has_permissions(administrator=True)
async def automod(ctx, action: str):
    """Enable or disable auto-moderation."""
    if action.lower() not in ['enable', 'disable']:
        await ctx.send("❌ Use: `/automod enable` or `/automod disable`", ephemeral=True)
        return
    
    bot.auto_mod_enabled[ctx.guild.id] = (action.lower() == 'enable')
    
    embed = discord.Embed(
        title="🛡️ Auto-Moderation " + ("Enabled" if action.lower() == 'enable' else "Disabled"),
        description="Auto-moderation will " + ("now automatically delete abusive messages and issue warnings." if action.lower() == 'enable' else "no longer automatically take action."),
        color=discord.Color.green() if action.lower() == 'enable' else discord.Color.red()
    )
    
    await ctx.send(embed=embed)


@bot.command(name='sync')
@commands.is_owner()
async def sync(ctx):
    """Manually sync slash commands (Owner only)."""
    try:
        synced = await bot.tree.sync()
        await ctx.send(f"✅ Synced {len(synced)} commands!")
    except Exception as e:
        await ctx.send(f"❌ Failed to sync: {e}")


@bot.hybrid_command(name='bothelp', description='Show all available commands')
async def help_command(ctx):
    """Show help."""
    embed = discord.Embed(
        title="🛡️ Guardify Help",
        description="Advanced Discord Moderation Bot",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="🛡️ Moderation Commands",
        value="`/warn` - Warn a user\n"
              "`/kick` - Kick a user\n"
              "`/ban` - Ban a user\n"
              "`/timeout` - Timeout a user\n"
              "`/purge` - Delete messages\n"
              "`/removewarn` - Remove a specific warning",
        inline=False
    )
    
    embed.add_field(
        name="🔍 Detection Commands",
        value="`/scan` - Scan a message\n"
              "`/history` - View abuse history\n"
              "`/stats` - View statistics\n"
              "`/warnings` - View user warnings\n"
              "`/clearwarnings` - Clear all warnings",
        inline=False
    )
    
    embed.add_field(
        name="⚙️ Settings",
        value="`/automod enable/disable` - Toggle auto-moderation",
        inline=False
    )
    
    embed.add_field(
        name="🤖 Auto Features",
        value="• Automatic abuse detection\n"
              "• Spam prevention\n"
              "• Forensics logging",
        inline=False
    )
    
    embed.set_footer(text="Use /command for detailed help on each command")
    
    await ctx.send(embed=embed)


def main():
    """Main entry point."""
    token = os.getenv('DISCORD_BOT_TOKEN')
    
    if not token:
        config_file = 'config.json'
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
                token = config.get('bot_token')
    
    if not token:
        print("ERROR: Discord bot token not found!")
        return
    
    bot.run(token)


if __name__ == "__main__":
    main()
