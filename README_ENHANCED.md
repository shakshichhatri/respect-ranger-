# 🛡️ Guardify - Advanced Discord Moderation Bot

<div align="center">

![Guardify Logo](https://img.shields.io/badge/Guardify-Discord%20Bot-7289DA?style=for-the-badge&logo=discord)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**AI-Powered Moderation • Real-Time Protection • Beautiful Dashboard**

[Features](#features) • [Installation](#installation) • [Commands](#commands) • [Dashboard](#dashboard) • [Support](#support)

</div>

---

## ✨ Features

### 🛡️ **Advanced Moderation**
- **Warn System** - Progressive warning system with automatic escalation
- **Kick & Ban** - Full moderation controls with reason tracking
- **Timeout** - Temporary mute functionality
- **Message Purge** - Bulk message deletion

### 🤖 **AI-Powered Detection**
- **Sentiment Analysis** - Detects toxic behavior using TextBlob
- **Keyword Detection** - Smart pattern matching for abusive content
- **Spam Prevention** - Automatic spam detection and prevention
- **Auto-Moderation** - Automatically handles abusive messages

### 📊 **Analytics & Logging**
- **Forensics Logging** - Complete audit trail of all moderation actions
- **Statistics Dashboard** - Real-time statistics and analytics
- **User History** - Track abuse history for individual users
- **Warning Tracking** - Persistent warning system across sessions

### 🎨 **User-Friendly Interface**
- **Rich Embeds** - Beautiful, colorful message embeds
- **Slash Commands** - Modern Discord slash command support
- **Web Dashboard** - Beautiful web interface for statistics
- **Status Updates** - Real-time bot status and activity

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Discord Bot Token ([Get one here](https://discord.com/developers/applications))
- Git (optional)

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/shakshichhatri/Guardify.git
cd Guardify
```

2. **Create virtual environment**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure bot**
```bash
# Copy config example
cp config.json.example config.json

# Edit config.json and add your bot token
{
  "bot_token": "YOUR_BOT_TOKEN_HERE",
  "command_prefix": "!",
  "log_directory": "forensics_logs"
}
```

5. **Run the enhanced bot**
```bash
python bot_enhanced.py
```

---

## 🚀 Quick Setup Guide

### 1. Create Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section and click "Add Bot"
4. Enable these **Privileged Gateway Intents**:
   - ✅ Message Content Intent
   - ✅ Server Members Intent
   - ✅ Presence Intent (optional)

### 2. Invite Bot to Server

Use this URL (replace `YOUR_CLIENT_ID`):
```
https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot&permissions=1099780063238
```

**Required Permissions:**
- View Channels
- Send Messages
- Manage Messages
- Kick Members
- Ban Members
- Timeout Members
- Read Message History

### 3. Enable Auto-Moderation

Once bot is running, use:
```
/automod enable
```

---

## 📝 Commands

### 🛡️ Moderation Commands

| Command | Description | Permission |
|---------|-------------|------------|
| `/warn @user [reason]` | Warn a user | Manage Messages |
| `/kick @user [reason]` | Kick a user from server | Kick Members |
| `/ban @user [reason]` | Ban a user from server | Ban Members |
| `/timeout @user <minutes> [reason]` | Timeout a user | Moderate Members |
| `/purge <amount>` | Delete multiple messages | Manage Messages |
| `/warnings @user` | View user's warnings | Manage Messages |
| `/clearwarnings @user` | Clear user's warnings | Administrator |

### 🔍 Detection Commands

| Command | Description | Permission |
|---------|-------------|------------|
| `/scan <message>` | Scan message for abuse | Manage Messages |
| `/history @user [limit]` | View abuse history | Manage Messages |
| `/stats` | View server statistics | Manage Messages |

### ⚙️ Configuration

| Command | Description | Permission |
|---------|-------------|------------|
| `/automod <enable/disable>` | Toggle auto-moderation | Administrator |
| `/help` | Show all commands | Everyone |

---

## 📊 Web Dashboard

### Features
- ✅ Real-time statistics
- ✅ Recent abuse cases
- ✅ Severity distribution charts
- ✅ Top warned users
- ✅ Beautiful, responsive design

### Running the Dashboard

```bash
python web_dashboard.py
```

Then open your browser to: `http://localhost:5000`

### Dashboard Screenshots

**Coming Soon!** - Beautiful analytics dashboard with:
- 📊 Real-time statistics
- 📈 Interactive charts
- 👥 User insights
- 🎨 Modern UI design

---

## 🎨 Bot Features Showcase

### Auto-Moderation in Action

```
User: "You're such an idiot"
Bot: ⚠️ Warning Issued
     Your message was removed for violating server rules.
     
     Reason: Abusive/Inappropriate Language
     Warnings: 1/3
     Severity: MEDIUM
```

### Rich Embed Messages

All bot responses use beautiful, color-coded embeds:
- 🟢 **Green** - Success/Safe messages
- 🟡 **Orange** - Warnings
- 🔴 **Red** - High severity/Bans
- 🔵 **Blue** - Information/Help

### Warning System

- **1st Warning** - Message deleted + warning
- **2nd Warning** - Message deleted + warning + final warning notice
- **3rd Warning** - 1 hour timeout + warning

---

## 🔧 Configuration

### config.json

```json
{
  "bot_token": "YOUR_BOT_TOKEN",
  "command_prefix": "!",
  "log_directory": "forensics_logs"
}
```

### Customization

You can customize:
- **Abuse Keywords** - Edit `abusive_keywords` in `bot_enhanced.py`
- **Thresholds** - Adjust `SENTIMENT_THRESHOLD` and `ABUSE_SCORE_THRESHOLD`
- **Warning Limits** - Modify warning escalation logic
- **Auto-mod Behavior** - Customize `handle_abusive_message` function

---

## 📁 File Structure

```
Guardify/
├── bot.py                  # Original bot (legacy)
├── bot_enhanced.py         # Enhanced moderation bot ⭐ USE THIS
├── web_dashboard.py        # Web dashboard server
├── config.json             # Bot configuration
├── requirements.txt        # Python dependencies
├── forensics_logs/         # Logs directory
│   ├── abuse_evidence.jsonl
│   └── warnings.json
├── templates/              # Web dashboard templates
│   └── dashboard.html
└── README_ENHANCED.md      # This file
```

---

## 🚦 Usage Examples

### Basic Moderation
```
/warn @BadUser Spamming links
/timeout @SpammerUser 30 Repeated spam
/kick @TrollUser Harassment
/ban @AbusiveUser Multiple violations
```

### Check User History
```
/history @SuspectUser 10
/warnings @SuspectUser
```

### Bulk Actions
```
/purge 50           # Delete last 50 messages
```

### Enable Protection
```
/automod enable     # Turn on auto-moderation
/stats              # View statistics
```

---

## 🛠️ Advanced Features

### Forensics Logging

All moderation actions are logged in JSON format:
```json
{
  "message_id": "123456789",
  "author_id": "987654321",
  "content": "Abusive message",
  "analysis": {
    "is_abusive": true,
    "severity": "high",
    "abuse_score": 0.85
  }
}
```

### API Integration

The web dashboard exposes a REST API at `/api/stats` for integration with other tools.

---

## 🤝 Support

### Getting Help

- 📖 Read the [Full Documentation](https://github.com/shakshichhatri/Guardify)
- 💬 Join our [Support Server](https://discord.gg/your-invite)
- 🐛 Report bugs on [GitHub Issues](https://github.com/shakshichhatri/Guardify/issues)

### Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🌟 Acknowledgments

- Built with [discord.py](https://github.com/Rapptz/discord.py)
- Sentiment analysis powered by [TextBlob](https://textblob.readthedocs.io/)
- UI inspired by modern Discord bots

---

## 📈 Roadmap

- [ ] Machine Learning model for better detection
- [ ] Multi-language support
- [ ] Custom command creation
- [ ] Integration with other bots
- [ ] Mobile app for dashboard
- [ ] Advanced analytics

---

<div align="center">

**Made with ❤️ for safer Discord communities**

[⬆ Back to Top](#-guardify---advanced-discord-moderation-bot)

</div>
