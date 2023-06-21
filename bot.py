import asyncio
import json
import random

import openai
from telethon import TelegramClient, events
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import PeerChannel, PeerUser, ReactionCustomEmoji

# Open AI.
openai.api_key = "<YOUR_TOKEN_HERE>"


# Telegram.
API_ID = 123456
API_HASH = "<YOUR_TOKEN_HERE>"

# Bot will be active only in these chats.
DIALOGS = {"Кросс-Зоопарк v2.0"}

# Generated mapping.
with open("mapping.json") as file:
    EMOJI_MAPPING: dict[str, list[int]] = json.load(file)


async def get_reaction(text: str) -> ReactionCustomEmoji | None:
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"{text}\n\nFor the text above choose single emoji that fits best and respond with only this "
                           f"emoji."
            }
        ],
        temperature=0,
        max_tokens=512
    )

    # Response from GPT.
    emoji = response["choices"][0]["message"]["content"]

    if emoji not in EMOJI_MAPPING:
        return None

    return ReactionCustomEmoji(document_id=random.choice(EMOJI_MAPPING[emoji]))


async def main() -> None:
    client = TelegramClient("./sessions/main", API_ID, API_HASH)
    await client.connect()
    print(f"Logged as: @{(await client.get_me()).username}")

    # Get ids for the dialogs when the bot will be enabled.
    chats = [dialog.id async for dialog in client.iter_dialogs() if dialog.name in DIALOGS]
    print(f"Enabled in ({len(chats)}) chats: {chats}, {DIALOGS}")

    @client.on(events.NewMessage(chats=chats))
    async def _wrapper(event: events.NewMessage.Event) -> None:
        if (
                not isinstance(event.message.from_id, PeerUser) or
                not isinstance(event.message.peer_id, PeerChannel) or
                event.message.text == ""
        ):
            return

        # if random.random() >= 0.5:
        #     print("Rate limited. Skipped.")
        #     return

        reaction = await get_reaction(event.message.text[:512])

        if reaction is None:
            print("Cannot determine reaction. Skipped.")
            return

        await client(
                SendReactionRequest(
                    peer=event.chat_id,
                    msg_id=event.message.id,
                    big=False,
                    add_to_recent=True,
                    reaction=[reaction]
                )
            )

    await asyncio.Future()
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
