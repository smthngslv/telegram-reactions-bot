# Telegram Reactions Bot

This bots acting as user-bot and send reactions to messages, using GPT3.

## Session
First of all you need to generate a telegram session (basically, login into your account). 

1. Login to your account in https://my.telegram.org/
2. Click under API Development tools. A Create new application window will appear.
3. A Create new application window will appear.
4. Fill in your application details. There is no need to enter any URL, and only the first two fields (App title and 
Short name) can currently be changed later. 
5. Click on Create application at the end. Remember that your API hash is secret and Telegram won’t let you revoke it. 
Don’t post it anywhere!
6. Log in. 
```shell
mkdir sessions
pip install -r requirenments.txt
python login.py <API_ID> <API_HASH>
```

## Run

1. First, generate mapping for emojis. Make sure, that you add a telegram token into the file.
```shell
python get_emojis.py
```

2. Then start the bot. Make sure, that you provide necessary tokens in file.
```shell
python bot.py
```
