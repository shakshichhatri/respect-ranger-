# 🚀 Guardify Quick Start Guide

## ✅ Your Bot is Now Running!

**Congratulations!** Your enhanced Guardify bot is online with powerful moderation features.

---

## 📋 What's New?

### 🛡️ **Advanced Moderation Features**
- ✅ `/warn` - Warning system with automatic escalation
- ✅ `/kick` - Kick users with reason tracking
- ✅ `/ban` - Ban users permanently
- ✅ `/timeout` - Temporarily mute users
- ✅ `/purge` - Bulk message deletion

### 🤖 **AI-Powered Protection**
- ✅ Automatic abuse detection
- ✅ Spam prevention (5+ messages in 5 seconds)
- ✅ Sentiment analysis
- ✅ Keyword filtering

### 📊 **Analytics & Tracking**
- ✅ `/stats` - View server statistics
- ✅ `/history` - User abuse history
- ✅ `/warnings` - View user warnings
- ✅ Complete forensics logging

### 🎨 **Beautiful UI**
- ✅ Rich colored embeds
- ✅ Slash commands support
- ✅ Web dashboard (see below)
- ✅ Status updates

---

## 🎯 First Steps

### 1. Enable Auto-Moderation

In your Discord server, type:
```
/automod enable
```

This will automatically:
- Delete abusive messages
- Issue warnings to users
- Timeout users after 3 warnings

### 2. Test the Bot

Try these commands:
```
/bothelp              # See all commands
/scan Your message    # Test abuse detection
/stats                # View statistics
```

### 3. Set Up Permissions

Make sure the bot has these permissions:
- ✅ Manage Messages
- ✅ Kick Members
- ✅ Ban Members
- ✅ Timeout Members

---

## 📊 Web Dashboard

### Start the Dashboard

Open a **NEW terminal** and run:
```bash
# Activate virtual environment first
.venv\Scripts\activate

# Run dashboard
python web_dashboard.py
```

Then open: **http://localhost:5000**

### Dashboard Features
- 📊 Real-time statistics
- 📈 Severity distribution charts
- 👥 Top warned users
- 📋 Recent abuse cases
- 🎨 Beautiful responsive design

---

## 💡 Command Examples

### Moderation
```
/warn @BadUser Spamming
/timeout @SpamUser 30 Repeated spam
/kick @TrollUser Harassment
/ban @AbusiveUser Severe violations
/purge 50
```

### Monitoring
```
/history @User 10           # Last 10 incidents
/warnings @User             # View warnings
/clearwarnings @User        # Clear all warnings
```

### Auto-Moderation
```
/automod enable             # Turn on auto-mod
/automod disable            # Turn off auto-mod
```

---

## 🔧 Configuration

### Customize Keywords

Edit `bot_enhanced.py` line ~30:
```python
self.abusive_keywords = [
    'hate', 'kill', 'stupid', # Add your own keywords
]
```

### Adjust Thresholds

Edit `bot_enhanced.py` lines 17-19:
```python
SENTIMENT_THRESHOLD = -0.3      # How negative is "bad"
ABUSE_SCORE_THRESHOLD = 0.4     # Overall abuse threshold
```

### Warning Escalation

Current system (edit in `handle_abusive_message`):
- **1st Warning** → Message deleted
- **2nd Warning** → Message deleted + final warning
- **3rd Warning** → 1 hour timeout

---

## 📝 Important Notes

### Slash Commands
- All commands work with `/` (slash commands)
- Slash commands auto-complete
- Some commands also work with `!` prefix

### Permissions
Commands check user permissions automatically:
- `/warn`, `/scan` → Manage Messages
- `/kick` → Kick Members
- `/ban` → Ban Members
- `/timeout` → Moderate Members
- `/automod` → Administrator

### Logging
All actions are logged in:
- `forensics_logs/abuse_evidence.jsonl` → Abuse cases
- `forensics_logs/warnings.json` → User warnings

---

## 🆘 Troubleshooting

### Commands Not Showing?
Wait 1-2 minutes for slash commands to sync, or:
```
/sync
```

### Bot Not Responding?
Check:
1. Bot is online (green status)
2. Bot has proper permissions
3. Commands are typed correctly

### Auto-Mod Not Working?
Make sure:
1. `/automod enable` was used
2. Bot has "Manage Messages" permission
3. Bot role is above user roles

---

## 🎨 Example Workflow

### Scenario: User Sends Abusive Message

**With Auto-Mod Enabled:**

1. User sends: "You're such an idiot"
2. Bot automatically:
   - Deletes the message
   - Issues warning (1/3)
   - Sends warning embed
   - Logs to forensics

3. After 3 warnings:
   - User gets 1-hour timeout
   - Moderators notified

**Manual Moderation:**

```
/history @BadUser           # Check their history
/warnings @BadUser          # View warnings
/timeout @BadUser 60        # Timeout for 1 hour
```

---

## 📈 Next Steps

1. **Join More Servers** - Use invite link to add bot to other servers
2. **Customize Settings** - Adjust thresholds and keywords
3. **Monitor Dashboard** - Check web dashboard regularly
4. **Train Your Team** - Teach moderators to use commands

---

## 🔗 Quick Links

- 📖 [Full Documentation](README_ENHANCED.md)
- 🐛 [Report Issues](https://github.com/shakshichhatri/Guardify/issues)
- 💬 [Support Server](https://discord.gg/your-invite)

---

## 🎉 You're All Set!

Your server is now protected by Guardify. The bot will:
- ✅ Monitor all messages 24/7
- ✅ Detect and log abuse automatically
- ✅ Take action when needed
- ✅ Provide detailed analytics

**Need help? Use `/bothelp` in Discord!**

---

<div align="center">

**Made with ❤️ for safer Discord communities**

</div>
