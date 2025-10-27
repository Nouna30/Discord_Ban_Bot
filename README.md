# Discord_Ban_Bot
#### 📋 Overview

**Auto-Ban Bot** is a Discord moderation bot designed to automatically **ban any user who sends a message in a protected channel**.
Its main purpose is to **protect servers from spammers or hacked accounts** by instantly banning offenders and cleaning up their recent messages.

### ⚙️ Features

*  Immediately bans anyone who sends a message in a restricted channel.
*  Deletes all messages sent by that user in the last 5 minutes.
*  Sends a direct message (DM) to the banned user explaining the reason.
*  Posts a warning message in the protected channel about the ban.
*  Saves bot activity and errors in a `discord.log` file for debugging.
*  Sends this logs into a specifice channel called log.

### 🧩 Requirements

**Python:**

* Python 3.10+

**Libraries:**

* `discord.py`
* `python-dotenv`

**Bot Permissions:**

* Ban Members
* Manage Messages
* Read Message History
* Send Messages

---

### 📦 Installation & Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Nouna30/Discord_Ban_Bot.git
   cd Discord_Ban_Bot
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file:** 

   ```env
   DISCORD_TOKEN=your_discord_bot_token
   PROTECTED_CHANNEL_ID=1425575887260352653
   LOG_CHANNEL_ID=1432473254349639880
   ```

4. **Run the bot:**

   ```bash
   python Banne_Bot.py
   ```
