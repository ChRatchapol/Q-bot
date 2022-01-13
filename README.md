# Q-bot
Q Bot is a queue management discord bot that can update result on google sheet also.

## Setup
This discord bot is using [Python](https://www.python.org/) and [discord.py](https://discordpy.readthedocs.io/en/stable/) with google sheet api.

### Install Python and dependencies
1. Go to [Python Download](https://www.python.org/downloads/) and download python and install it. **(don't forget to put python in to environment path)** 
2. Use `pip install [package]` to install following packages. **(Use python, python3 or py and make sure that you install in correct version of python.)**

|command                                     |link                                                                          |
|--------------------------------------------|------------------------------------------------------------------------------|
|`py -m pip install discord.py`              |[discord.py](https://pypi.org/project/discord.py/)                            |
|`py -m pip install python-dotenv`           |[python-dotenv](https://pypi.org/project/python-dotenv/)                      |
|`py -m pip install google-api-python-client`|[google-api-python-client](https://pypi.org/project/google-api-python-client/)|
|`py -m pip install google-auth-httplib2`    |[google-auth-httplib2](https://pypi.org/project/google-auth-httplib2/)        |
|`py -m pip install google-auth-oauthlib`    |[google-auth-oauthlib](https://pypi.org/project/google-auth-oauthlib/)        |

### Setup Discord Bot
1. Go to [Discord Developer Portal](https://discord.com/developers/applications). (and of course you have to have discord account first!)
2. Click **New Application** button. (right now it is at top right next to your profile)
3. Enter your bot's name and click **Create**.
4. Go to **OAuth2** tab and **URL Generator** tab.
5. Check **bot** in **scope**.
6. Check following permissions. **(Your permission should be 532844899440 in the URL.)**
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
8. Open it in new tab and authorize your bot to enter your server. (Create empty server to test it first if you're unsure.)
9. Go back to [Discord Developer Portal](https://discord.com/developers/applications) page and go to **Bot**  tab.
10. Copy your bot's **Token** for [.env](#env-file) file. **This is (likely) your bot's password. Do not expose it to the public.** (below your bot's username)

### Setup Google Cloud Platform
1. Go to [Google Developer Console](https://console.cloud.google.com/apis/dashboard) and login with your account.
2. Create new project.
3. Enter your project name. (maybe as same as the bot) You can fill everything else as you please. Then click **Create**.
4. Make sure you activate it by clicking it on notification once it done loading. (Or you could open it from drop down menu up top.)
5. On the top left of the page, you should see the menu icon (3 horizontal lines or hamburger if you like the name). Click it and go to **APIs & Services** then click on "**+ ENABLE APIS AND SERVICES**" up top.
6. Search for **sheet** and then **Google Sheet API** should show up. Click it and enable it.
7. Go to the hamburger menu then go to **IAM & Admin** tab. Go to **Service Accounts** tab on the left and click "**+ CREATE SERVICE ACCOUNT**".
8. Enter service account name (maybe as same as the bot) and click create. (You can fill everything else if you want.)
9. Set a role of the service account from drop down menu to be **Editor** then click **CONTINUE** and **DONE**.
10. You should be back at **Service Account** page and it should has the service account you just create. Copy it's email.
11. Go to Google Sheet you want the bot to access then share it with email you just copied. (You should check that you've shared it with **editor** permission.)
12. Go back to [Google Developer Console](https://console.cloud.google.com/apis/dashboard). On the **Service Accounts** tab in **IAM & Admin** click on email you just copy. It should bring you to service account details page.
13. At the bottom of the page, click on **ADD KEY** drop down menu and choose **Create new key**. Choose **JSON** and click **CREATE**. This should download the key file to your computer, place it in the **ggsheet** folder with "**keys.json**" name. (**This key is like the discord bot's token, it should not be expose to the public.**)

## .env file
create .env file and add following content to the file
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

### Reference
[ref](./REF.md)