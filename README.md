# Q-bot
Q Bot is a queue management discord bot that can update result on google sheet also.

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

## keys.json
create key for your Google Service Account and place the file in ggsheet folder (also rename it to keys.json)

### Reference
[ref](./ref.txt)