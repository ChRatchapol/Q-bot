# Q-bot
Q Bot is a queue management discord bot that can update the queue on a google sheet.

## Setup
This discord bot uses [Python](https://www.python.org/) and [discord.py](https://discordpy.readthedocs.io/en/stable/) with google sheet API.

### Install Python and dependencies
1. Go to [Python Download](https://www.python.org/downloads/) and download python and install it. **(don't forget to put python into the environment path)** 
2. Use `pip install [package]` to install the following packages. **(Use python, python3, or py and make sure that it will install on the correct version.)**

|command                                     |link                                                                          |
|--------------------------------------------|------------------------------------------------------------------------------|
|`py -m pip install discord.py`              |[discord.py](https://pypi.org/project/discord.py/)                            |
|`py -m pip install python-dotenv`           |[python-dotenv](https://pypi.org/project/python-dotenv/)                      |
|`py -m pip install google-api-python-client`|[google-api-python-client](https://pypi.org/project/google-api-python-client/)|
|`py -m pip install google-auth-httplib2`    |[google-auth-httplib2](https://pypi.org/project/google-auth-httplib2/)        |
|`py -m pip install google-auth-oauthlib`    |[google-auth-oauthlib](https://pypi.org/project/google-auth-oauthlib/)        |

### Setup Discord Bot
1. Go to [Discord Developer Portal](https://discord.com/developers/applications). (and of course, you have to have a discord account first!)
2. Click the **New Application** button. (Right now, it is at the top right next to your profile)
3. Enter your bot's name and click **Create**.
4. Go to the **OAuth2** tab and **URL Generator** tab.
5. Check **bot** in **scope**.
6. Check the following permissions. **(Your bot's permission should be 532844899440 in the URL.)**
    * Manage Server
    * Manage Roles
    * Manage Channels
    * Read Messages/View Channels
    * Send Messages
    * Create Public Threads
    * Create Private Threads
    * Send Messages in Threads
    * Manage Messages
    * Manages Threads
    * Embed Links
    * Attach Files
    * Read Messages History
    * Mention Everyone
    * Use External Emojis
    * Use External Stickers
    * Add Reactions
7. Copy the URL at the bottom of the page.
8. Open it in a new tab and authorize your bot to enter your server. (Create an empty server to test it first if you're unsure.)
9. Go back to the [Discord Developer Portal](https://discord.com/developers/applications) page and go to the **Bot**  tab.
10. Copy your bot's **Token** for [.env](#env-file) file. **The Token is (likely) your bot's password. Do not expose it to the public.** (below your bot's username)

### Setup Google Cloud Platform
1. Go to [Google Developer Console](https://console.cloud.google.com/apis/dashboard) and log in with your account.
2. Create a new project.
3. Enter your project name. (maybe as same as the bot) You can fill everything else as you please. Then click **Create**.
4. Make sure you activate it by clicking on the notification once it is loaded. (Or you could open it from the drop-down menu up top.)
5. On the top left of the page, you should see the menu icon (3 horizontal lines or hamburger if you like the name). Click it and go to **APIs & Services** then, click on "**+ ENABLE APIS AND SERVICES**" up top.
6. Search for **sheet** and, **Google Sheet API** should show up. Click it and enable it.
7. Go to the hamburger menu then, go to **IAM & Admin** tab. Go to the **Service Accounts** tab on the left and click "**+ CREATE SERVICE ACCOUNT**".
8. Enter a service account name (maybe as same as the bot) and click create. (You can fill everything else if you want.)
9. Set a role of the service account from the drop-down menu to be **Editor** then, click **CONTINUE** and **DONE**.
10. You should be back on the **Service Account** page and, it should have the service account you created. Copy its email.
11. Go to the spreadsheet (Google Sheet) you want the bot to access then, share it with the email you just copied. (You should check that you've shared it with **editor** permission.)
12. Go back to [Google Developer Console](https://console.cloud.google.com/apis/dashboard). On the **Service Accounts** tab in **IAM & Admin**, click on the email you copied. It should bring you to the service account details page.
13. At the bottom of the page, click on the **ADD KEY** drop-down menu and choose **Create new key**. Choose **JSON** and click **CREATE**. It should start downloading the key file to your computer, place it in the **ggsheet** folder with the "**keys.json**" name. (**This key is like the discord bot's token. It should not expose to the public.**)

### .env file
Create a .env file and add the following content to the file.
```
ADMIN_ROLE=TA
COMMAND_PREFIX=$
COMMAND_LIST=["add","remove","list","next","help"]
DISCORD_BOT_TOKEN=[your discord bot token]
QUEUE_FILE_NAME=[your queue file name]
SPREADSHEET_ID=[your spreadsheet id]
```

For `DISCORD_BOT_TOKEN`, you should look at [Setup Discord Bot](#setup-discord-bot).

For `SPREADSHEET_ID`, it is on the URL of the spreadsheet. (after ...d/ and before /edit...) 

### Google Sheet
You can use any google sheet (that you already shared to the google service account) but, the sheet name must be "**Queue**".

## Usage
Once, The bot is in the discord server. You can run the code by running `main.py` (not `main.py` in the ggsheet folder) by typing `py main.py`. (make sure that you use the correct version of python)

The bot should start working. It will scan through all servers that it can access and create **TA** role, **Q Bot** category and, all text channels needed. (If you already have role, category or text channels, it won't do anything.)

After that, the bot is ready to go. You can use the following commands.
**I strongly recommend you to use `$help` first.**

|command                            |description                                   |
|-----------------------------------|----------------------------------------------|
|$add "[group name]" "[topic]"**\***|add group name and topic to the queue         |
|$remove "[group name]"**\***       |remove group name and its topic from the queue|
|$list                              |list all queue                                |
|$next                              |pop item from the queue                       |
|$help                              |show help message                             |
**\*** Double-quotes (") is needed.

### Reference
[ref](./REF.md)